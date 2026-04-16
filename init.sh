#!/usr/bin/env bash
set -euo pipefail

# Simple backend bootstrap for remote machine (run from story_gen_django/)
# - Starts Postgres, Redis, Django via docker compose (with GPU override)
# - Applies migrations
# - Sets up JoyCaption2 (TripleX) inside the web container
# - Persists model/cache directories to avoid repeated downloads

# Usage: from story_gen_django directory
#   bash init.sh

###############################
# Docker/Compose prerequisites
###############################

INSTALL_DEPS=false
NON_INTERACTIVE=false
WITH_GPU=false
WITH_LOCAL_DB=false
WITH_LOCAL_REDIS=false
WRITE_OVERRIDE=false
CHECK_ONLY=false
HOST_WEB=false
AUTO_HOST_WEB=false

while [[ ${1:-} =~ ^- ]]; do
  case "${1}" in
    --install-deps)
      INSTALL_DEPS=true
      shift
      ;;
    --non-interactive|--yes|-y)
      NON_INTERACTIVE=true
      shift
      ;;
    --gpu)
      WITH_GPU=true
      shift
      ;;
    --with-local-db)
      WITH_LOCAL_DB=true
      shift
      ;;
    --with-local-redis)
      WITH_LOCAL_REDIS=true
      shift
      ;;
    --write-override)
      WRITE_OVERRIDE=true
      shift
      ;;
    --host-web)
      HOST_WEB=true
      shift
      ;;
    --auto-host-web)
      AUTO_HOST_WEB=true
      shift
      ;;
    --check)
      CHECK_ONLY=true
      shift
      ;;
    -h|--help)
      cat <<USAGE
Usage: bash init.sh [--install-deps] [--non-interactive] [--gpu] [--with-local-db] [--with-local-redis] [--write-override] [--host-web] [--auto-host-web] [--check]

Options:
  --install-deps     Attempt to install Docker and Compose if missing.
  --non-interactive  Do not prompt; assume yes to installs (CI-friendly).
  --gpu              Enable GPU override compose file if host supports it.
  --with-local-db    Force starting local db service (ignores DB_HOST).
  --with-local-redis Force starting local redis service (ignores REDIS_URL).
  --write-override   Generate docker-compose.override.yml (extra_hosts pin / host networking).
  --host-web         Force web service to use host networking (IPv6 via host).
  --auto-host-web    If DB host has no IPv4 and host has IPv6, auto host-network the web service.
  --check            Run preflight checks only and exit.
  -h, --help         Show this help message.
USAGE
      exit 0
      ;;
    *)
      echo "Unknown option: ${1}" >&2
      exit 1
      ;;
  esac
done

prompt_yes_no() {
  local msg="$1"
  if $NON_INTERACTIVE; then
    return 0
  fi
  read -r -p "$msg [Y/n] " ans || true
  case "${ans:-Y}" in
    [Yy]*|"") return 0 ;;
    *) return 1 ;;
  esac
}

detect_os() {
  OS_FAMILY="unknown"
  OS_ID=""
  OS_VERSION_ID=""
  if [[ "$(uname -s)" == "Darwin" ]]; then
    OS_FAMILY="darwin"
  elif [[ -f /etc/os-release ]]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    OS_ID="${ID:-}"
    OS_VERSION_ID="${VERSION_ID:-}"
    case "${ID_LIKE:-$ID}" in
      *debian*|*ubuntu*) OS_FAMILY="debian" ;;
      *rhel*|*centos*|*fedora*) OS_FAMILY="rhel" ;;
      *amzn*|*amazon*) OS_FAMILY="amazon" ;;
      *fedora*) OS_FAMILY="rhel" ;;
      *) OS_FAMILY="$ID" ;;
    esac
  fi
}

# Safely set or update a key in .env
set_env_kv() {
  local key="$1" val="$2"
  if grep -qE "^${key}=" .env; then
    # Portable in-place edit
    tmp_file=$(mktemp)
    awk -v k="${key}" -v v="${val}" 'BEGIN{set=0} {if($0 ~ "^"k"="){if(!set){print k"="v; set=1}} else {print}} END{if(!set){print k"="v}}' .env > "$tmp_file"
    mv "$tmp_file" .env
  else
    echo "${key}=${val}" >> .env
  fi
}

resolve_ipv4() {
  local host="$1"
  local ip=""
  # 1) System resolver (glibc)
  if command -v getent >/dev/null 2>&1; then
    ip=$(getent ahostsv4 "$host" | awk 'NR==1{print $1}') || true
  fi
  # 2) dig via system resolver
  if [[ -z "$ip" ]] && command -v dig >/dev/null 2>&1; then
    ip=$(dig +short A "$host" | head -n1) || true
  fi
  # 3) dig via Cloudflare
  if [[ -z "$ip" ]] && command -v dig >/dev/null 2>&1; then
    ip=$(dig +short A "$host" @1.1.1.1 | head -n1) || true
  fi
  # 4) dig via Google
  if [[ -z "$ip" ]] && command -v dig >/dev/null 2>&1; then
    ip=$(dig +short A "$host" @8.8.8.8 | head -n1) || true
  fi
  # 5) DNS-over-HTTPS (Cloudflare)
  if [[ -z "$ip" ]] && command -v curl >/dev/null 2>&1; then
    ip=$(curl -fsSL "https://1.1.1.1/dns-query?name=${host}&type=A" -H 'accept: application/dns-json' \
      | grep -oE '"data":"([0-9]{1,3}(\.[0-9]{1,3}){3})"' | head -n1 | sed -E 's/.*"data":"([0-9.]+)".*/\1/') || true
  fi
  # 6) DNS-over-HTTPS (Google)
  if [[ -z "$ip" ]] && command -v curl >/dev/null 2>&1; then
    ip=$(curl -fsSL "https://dns.google/resolve?name=${host}&type=A" \
      | grep -oE '"data":"([0-9]{1,3}(\.[0-9]{1,3}){3})"' | head -n1 | sed -E 's/.*"data":"([0-9.]+)".*/\1/') || true
  fi
  echo "$ip"
}

ensure_tool() {
  local bin="$1" install_cmd="$2"
  if ! command -v "$bin" >/dev/null 2>&1; then
    if $INSTALL_DEPS; then
      eval "$install_cmd" || true
    fi
  fi
}

# Return non-empty output if host has working outbound IPv6
host_has_ipv6() {
  if command -v curl >/dev/null 2>&1; then
    curl -6 -s --max-time 2 https://api64.ipify.org || true
  fi
}

preflight_db_connectivity() {
  local host="$1" port="$2" hostaddr="$3"
  local target_ip="$hostaddr"
  if [[ -z "$target_ip" ]]; then
    target_ip=$(resolve_ipv4 "$host")
  fi
  if [[ -z "$target_ip" ]]; then
    echo "DB preflight: could not resolve IPv4 for $host (will continue)." >&2
    return 0
  fi
  detect_os
  if [[ "$OS_FAMILY" == "amazon" || "$OS_FAMILY" == "rhel" ]]; then
    ensure_tool nc "sudo dnf install -y nmap-ncat || sudo yum install -y nmap-ncat"
  elif [[ "$OS_FAMILY" == "debian" ]]; then
    ensure_tool nc "sudo apt-get update -y && sudo apt-get install -y netcat-openbsd"
  fi
  if command -v nc >/dev/null 2>&1; then
    if nc -z -w3 "$target_ip" "$port"; then
      echo "DB preflight: $host ($target_ip:$port) reachable."
      return 0
    else
      echo "DB preflight: cannot reach $host ($target_ip:$port)." >&2
      return 1
    fi
  else
    echo "DB preflight: nc not available; skipping reachability test." >&2
    return 0
  fi
}

ensure_db_ipv4_ssl() {
  # Read .env
  local host port sslmode hostaddr
  host=$(grep -E '^DB_HOST=' .env | head -n1 | cut -d'=' -f2- || echo "")
  port=$(grep -E '^DB_PORT=' .env | head -n1 | cut -d'=' -f2- || echo "5432")
  sslmode=$(grep -E '^DB_SSLMODE=' .env | head -n1 | cut -d'=' -f2- || echo "")
  hostaddr=$(grep -E '^DB_HOSTADDR=' .env | head -n1 | cut -d'=' -f2- || echo "")

  [[ -z "$host" ]] && host="db"
  # If using Supabase or other managed hosts, default sslmode=require
  if [[ -z "$sslmode" ]] && [[ "$host" =~ supabase\.co$ ]]; then
    set_env_kv DB_SSLMODE require
  fi

  # If DB_HOST is not local and hostaddr empty, try to resolve IPv4 and set hostaddr
  if [[ "$host" != "db" && "$host" != "localhost" && "$host" != "127.0.0.1" ]] && [[ -z "$hostaddr" ]]; then
    # Ensure dig present to maximize resolution chances
    detect_os
    if [[ "$OS_FAMILY" == "amazon" || "$OS_FAMILY" == "rhel" ]]; then
      ensure_tool dig "sudo dnf install -y bind-utils || sudo yum install -y bind-utils"
    elif [[ "$OS_FAMILY" == "debian" ]]; then
      ensure_tool dig "sudo apt-get update -y && sudo apt-get install -y dnsutils"
    fi
    local ip
    ip=$(resolve_ipv4 "$host")
    if [[ -n "$ip" ]]; then
      set_env_kv DB_HOSTADDR "$ip"
      hostaddr="$ip"
    fi
  fi

  # Determine if we should place web on host network (useful for IPv6-only DB hosts)
  local use_host_net=false
  if $HOST_WEB; then
    use_host_net=true
  elif $AUTO_HOST_WEB; then
    if [[ "$host" != "db" && "$host" != "localhost" && "$host" != "127.0.0.1" ]] && [[ -z "$hostaddr" ]]; then
      # No IPv4 A record; if host has IPv6, prefer host networking so container inherits host IPv6 stack
      local hv6
      hv6=$(host_has_ipv6)
      if [[ -n "$hv6" ]]; then
        use_host_net=true
      fi
    fi
  fi

  # Optional compose override with extra_hosts and/or host networking
  if $WRITE_OVERRIDE && { [[ -n "${hostaddr}" ]] || $use_host_net; }; then
    {
      echo "version: '3.8'"
      echo "services:"
      echo "  web:"
      if $use_host_net; then
        echo "    network_mode: host"
        echo "    ports: []"
      fi
      if [[ -n "${hostaddr}" ]]; then
        echo "    extra_hosts:"
        echo "      - \"${host}:${hostaddr}\""
      fi
    } > docker-compose.override.yml
    if $use_host_net && [[ -n "${hostaddr}" ]]; then
      echo "Wrote docker-compose.override.yml (host network for web; pinned ${host} -> ${hostaddr})"
    elif $use_host_net; then
      echo "Wrote docker-compose.override.yml (host network for web due to IPv6-only DB host)"
    else
      echo "Wrote docker-compose.override.yml to pin ${host} -> ${hostaddr}"
    fi
  fi

  # Preflight connectivity (best-effort)
  preflight_db_connectivity "$host" "$port" "$hostaddr" || true
}

retry() {
  local attempts=$1; shift
  local sleep_s=$1; shift
  local n=0
  until "$@"; do
    n=$((n+1))
    if (( n >= attempts )); then
      return 1
    fi
    sleep "$sleep_s"
  done
}

ensure_docker_running() {
  if command -v systemctl >/dev/null 2>&1; then
    if ! systemctl is-active --quiet docker 2>/dev/null; then
      sudo systemctl enable --now docker || true
    fi
  fi
}

install_docker_engine_linux() {
  case "$1" in
    debian)
      sudo apt-get update -y
      # Prefer distro docker for simplicity
      sudo apt-get install -y docker.io || true
      ;;
    rhel)
      if command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y docker || sudo dnf install -y docker-ce || true
      else
        sudo yum install -y docker || sudo yum install -y docker-ce || true
      fi
      ;;
    amazon)
      # Amazon Linux 2 vs 2023 paths
      if [[ "${OS_VERSION_ID:-}" =~ ^2(\.|$) ]]; then
        sudo amazon-linux-extras enable docker || true
        sudo yum install -y docker || true
      else
        sudo dnf install -y docker || sudo dnf install -y docker-ce || true
      fi
      ;;
    *)
      echo "Unrecognized Linux family '$1'. Attempting generic install of docker.io..." >&2
      sudo apt-get update -y || true
      sudo apt-get install -y docker.io || true
      ;;
  esac
}

install_compose_linux_plugin() {
  case "$1" in
    debian)
      sudo apt-get update -y
      sudo apt-get install -y docker-compose-plugin || true
      if ! docker compose version >/dev/null 2>&1; then
        download_compose_plugin_binary
      fi
      ;;
    rhel)
      if command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y docker-compose-plugin || true
      else
        sudo yum install -y docker-compose-plugin || true
      fi
      if ! docker compose version >/dev/null 2>&1; then
        download_compose_plugin_binary
      fi
      ;;
    amazon)
      if command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y docker-compose-plugin || true
      else
        # Fallback: download plugin
        download_compose_plugin_binary
      fi
      # If dnf path didn't provide the plugin, fallback to binary
      if ! docker compose version >/dev/null 2>&1; then
        download_compose_plugin_binary
      fi
      ;;
    *)
      # Generic fallback
      download_compose_plugin_binary
      ;;
  esac
}

download_compose_plugin_binary() {
  local arch
  arch=$(uname -m)
  local bin="linux-x86_64"
  if [[ "$arch" == "aarch64" || "$arch" == "arm64" ]]; then
    bin="linux-aarch64"
  fi
  local url="https://github.com/docker/compose/releases/download/v2.27.1/docker-compose-${bin}"
  echo "Downloading docker compose plugin from $url ..."
  sudo mkdir -p /usr/local/lib/docker/cli-plugins
  sudo curl -fsSL "$url" -o /usr/local/lib/docker/cli-plugins/docker-compose
  sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
}

ensure_gpu_runtime() {
  # Attempt to ensure host GPU runtime (driver + nvidia-container-toolkit) when requested.
  # Safe best-effort: only runs when --gpu and --install-deps flags are used.
  if ! $WITH_GPU || ! $INSTALL_DEPS; then
    return 0
  fi

  if command -v nvidia-smi >/dev/null 2>&1; then
    # GPU driver present; ensure container toolkit exists
    if ! command -v nvidia-ctk >/dev/null 2>&1 && ! command -v nvidia-container-toolkit >/dev/null 2>&1; then
      detect_os
      case "$OS_FAMILY" in
        debian)
          sudo apt-get update -y || true
          sudo apt-get install -y nvidia-container-toolkit || true
          ;;
        rhel|amazon)
          if command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y nvidia-container-toolkit || true
          else
            sudo yum install -y nvidia-container-toolkit || true
          fi
          ;;
      esac
      if command -v nvidia-ctk >/dev/null 2>&1; then
        sudo nvidia-ctk runtime configure --runtime=docker || true
        sudo systemctl restart docker || true
      fi
    fi
    return 0
  fi

  # nvidia-smi missing: try to install both driver and container toolkit (best-effort).
  detect_os
  case "$OS_FAMILY" in
    debian)
      if prompt_yes_no "Install NVIDIA driver + container toolkit (Debian/Ubuntu)?"; then
        sudo apt-get update -y || true
        # Driver version may vary; 535 is widely available. Adjust if necessary.
        sudo apt-get install -y nvidia-driver-535 || true
        sudo apt-get install -y nvidia-container-toolkit || true
        if command -v nvidia-ctk >/dev/null 2>&1; then
          sudo nvidia-ctk runtime configure --runtime=docker || true
        fi
        sudo systemctl restart docker || true
      fi
      ;;
    rhel|amazon)
      if prompt_yes_no "Install NVIDIA driver + container toolkit (RHEL/Amazon Linux)?"; then
        if command -v dnf >/dev/null 2>&1; then
          # Add CUDA repo (RHEL9 compatible) to get nvidia-driver on AL2023 or RHEL9
          sudo dnf -y install dnf-plugins-core || true
          sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/cuda-rhel9.repo || true
          sudo dnf clean all || true
          # Install driver (may require reboot to load kernel modules)
          sudo dnf install -y nvidia-driver nvidia-modprobe || sudo dnf install -y akmod-nvidia || true

          # Add NVIDIA libnvidia-container repo (use RHEL9 feed as fallback on AL2023)
          if [[ ! -f /etc/yum.repos.d/libnvidia-container.repo ]]; then
            sudo curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /etc/pki/rpm-gpg/NVIDIA-CONTAINER-GPG-KEY || true
            sudo curl -fsSL https://nvidia.github.io/libnvidia-container/stable/rpm/rhel9/libnvidia-container.repo | sudo tee /etc/yum.repos.d/libnvidia-container.repo >/dev/null || true
            sudo dnf clean all || true
          fi
          sudo dnf install -y nvidia-container-toolkit || true
        else
          # yum fallback (older distros)
          sudo yum install -y nvidia-driver || true
          sudo yum install -y nvidia-container-toolkit || true
        fi
        if command -v nvidia-ctk >/dev/null 2>&1; then
          sudo nvidia-ctk runtime configure --runtime=docker || true
        fi
        sudo systemctl restart docker || true
        echo "NOTE: A host reboot may be required for NVIDIA kernel modules to load (nvidia-smi)." >&2
      fi
      ;;
  esac

  # Re-check
  if command -v nvidia-smi >/dev/null 2>&1; then
    echo "GPU driver detected after setup." 
  else
    echo "WARNING: NVIDIA driver still not detected. GPU will not be available to containers." >&2
  fi
}

###############################
# Auto-configuration for AWS DLAMI
###############################

detect_and_configure_dlami_storage() {
  echo "=== Detecting AWS DLAMI ephemeral storage ==="

  # Check if ephemeral NVMe storage exists
  if [[ ! -d "/opt/dlami/nvme" ]]; then
    echo "Not running on AWS DLAMI (no /opt/dlami/nvme found). Skipping storage optimization."
    return 0
  fi

  # Check available space on ephemeral disk
  local available_gb=$(df -BG /opt/dlami/nvme 2>/dev/null | awk 'NR==2 {print $4}' | sed 's/G//' || echo "0")
  echo "DLAMI ephemeral storage detected: ${available_gb}GB available"

  if [[ $available_gb -lt 50 ]]; then
    echo "Ephemeral storage has less than 50GB available. Skipping Docker relocation."
    return 0
  fi

  # Check if Docker is already configured for ephemeral storage
  local current_root=$(docker info 2>/dev/null | grep "Docker Root Dir" | awk '{print $4}' || echo "")
  if [[ "$current_root" == "/opt/dlami/nvme/docker" ]]; then
    echo "Docker already configured for ephemeral storage at $current_root"
    return 0
  fi

  echo "Configuring Docker to use ephemeral storage (${available_gb}GB available)..."

  # Stop Docker daemon
  echo "Stopping Docker daemon..."
  sudo systemctl stop docker || true
  sleep 2

  # Create directory on ephemeral disk
  sudo mkdir -p /opt/dlami/nvme/docker

  # Move existing Docker data if present
  if [[ -d "/var/lib/docker" && ! -L "/var/lib/docker" ]]; then
    echo "Moving existing Docker data to ephemeral storage..."
    sudo rsync -a /var/lib/docker/ /opt/dlami/nvme/docker/ || echo "Warning: rsync had errors, continuing..."
    sudo mv /var/lib/docker /var/lib/docker.backup.$(date +%Y%m%d_%H%M%S)
  fi

  # Update daemon.json using Python
  echo "Updating Docker daemon configuration..."
  sudo python3 << 'PYTHON_EOF'
import json
import os

daemon_json_path = "/etc/docker/daemon.json"

# Read existing config or create empty
if os.path.exists(daemon_json_path):
    try:
        with open(daemon_json_path, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        config = {}
else:
    config = {}

# Update data-root
config["data-root"] = "/opt/dlami/nvme/docker"

# Write back
with open(daemon_json_path, 'w') as f:
    json.dump(config, f, indent=2)

print(f"Updated {daemon_json_path}")
PYTHON_EOF

  # Start Docker
  echo "Starting Docker daemon with new configuration..."
  sudo systemctl start docker
  sleep 3

  # Verify
  local new_root=$(docker info 2>/dev/null | grep "Docker Root Dir" | awk '{print $4}' || echo "unknown")
  echo "Docker Root Dir is now: $new_root"

  if [[ "$new_root" == "/opt/dlami/nvme/docker" ]]; then
    echo "✓ Successfully configured Docker to use ephemeral storage"
  else
    echo "⚠ Warning: Docker Root Dir verification failed, may need manual check"
  fi
}

detect_and_configure_ipv6() {
  echo "=== Detecting IPv6 requirements ==="

  # Extract database hostname from environment
  local db_host="${DATABASE_URL:-}"
  if [[ -z "$db_host" ]]; then
    # Try various common environment variables
    db_host="${DB_HOST:-}"
  fi

  # If still empty, try to find Supabase host in files
  if [[ -z "$db_host" ]]; then
    db_host=$(grep -h "supabase.co" docker-compose*.yml .env* 2>/dev/null | grep -oE '(db\.)?[a-z0-9-]+\.supabase\.co' | head -1 || echo "")
  fi

  if [[ -z "$db_host" ]]; then
    echo "No external database host detected. Skipping IPv6 configuration."
    return 0
  fi

  echo "Database host detected: $db_host"

  # Check for IPv6 (AAAA) and IPv4 (A) records
  local has_ipv6=$(dig +short "$db_host" AAAA 2>/dev/null | head -1)
  local has_ipv4=$(dig +short "$db_host" A 2>/dev/null | head -1)

  if [[ -z "$has_ipv6" ]]; then
    echo "Database does not have IPv6 address. Skipping IPv6 configuration."
    return 0
  fi

  echo "Database has IPv6 address: $has_ipv6"

  if [[ -n "$has_ipv4" ]]; then
    echo "Database also has IPv4 address: $has_ipv4"
    echo "Enabling IPv6 for compatibility..."
  else
    echo "Database is IPv6-only. IPv6 support is REQUIRED."
  fi

  # Check if IPv6 already enabled in Docker
  local ipv6_enabled=$(docker network inspect bridge 2>/dev/null | grep -i "EnableIPv6" | grep "true" || echo "")
  if [[ -n "$ipv6_enabled" ]]; then
    echo "IPv6 already enabled in Docker bridge network"
  else
    echo "Enabling IPv6 in Docker daemon..."
    enable_docker_ipv6
  fi

  # Configure docker-compose.yml network
  configure_compose_ipv6_network
}

enable_docker_ipv6() {
  echo "Configuring Docker daemon for IPv6..."

  # Stop Docker
  sudo systemctl stop docker || true
  sleep 2

  # Update daemon.json using Python
  sudo python3 << 'PYTHON_EOF'
import json
import os

daemon_json_path = "/etc/docker/daemon.json"

# Read existing config
if os.path.exists(daemon_json_path):
    try:
        with open(daemon_json_path, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        config = {}
else:
    config = {}

# Add IPv6 configuration
config["ipv6"] = True
config["fixed-cidr-v6"] = "fd01::/80"

# Write back
with open(daemon_json_path, 'w') as f:
    json.dump(config, f, indent=2)

print(f"Updated {daemon_json_path} with IPv6 support")
PYTHON_EOF

  # Start Docker
  echo "Restarting Docker daemon..."
  sudo systemctl start docker
  sleep 3

  echo "✓ IPv6 enabled in Docker daemon"
}

configure_compose_ipv6_network() {
  local compose_file="docker-compose.yml"

  # Check if networks section exists
  if grep -q "^networks:" "$compose_file"; then
    echo "Networks section found in $compose_file"

    # Check for problematic configurations
    if grep -q "subnet.*172\.19\.0\.0/16" "$compose_file"; then
      echo "⚠ Found hardcoded IPv4 subnet causing conflicts - removing and rebuilding networks section..."
      sed -i.bak '/^networks:/,$d' "$compose_file"
      # Fall through to add correct config
    elif grep -q "subnet.*fd01::/80" "$compose_file"; then
      echo "⚠ Found fd01::/80 subnet conflicting with daemon.json - updating to fd02::/80..."
      sed -i.bak 's|subnet: fd01::/80|subnet: fd02::/80|' "$compose_file"
      echo "✓ Updated IPv6 subnet to avoid conflict"
      return 0
    elif grep -q "enable_ipv6.*true" "$compose_file"; then
      echo "✓ IPv6 already properly configured in docker-compose.yml"
      return 0
    else
      echo "⚠ Networks section exists but IPv6 not enabled - removing and rebuilding..."
      sed -i.bak '/^networks:/,$d' "$compose_file"
      # Fall through to add correct config
    fi
  fi

  echo "Adding IPv6 network configuration to $compose_file..."

  # Append networks section - let Docker auto-allocate IPv4 to avoid conflicts
  # Use fd02::/80 instead of fd01::/80 to avoid conflict with daemon.json default bridge allocation
  cat >> "$compose_file" << 'COMPOSE_EOF'

networks:
  default:
    enable_ipv6: true
    ipam:
      config:
        - subnet: fd02::/80
COMPOSE_EOF

  echo "✓ Added IPv6 network configuration to docker-compose.yml"
}

ensure_docker_and_compose() {
  detect_os

  if ! command -v docker >/dev/null 2>&1; then
    echo "Docker not found."
    if [[ "$OS_FAMILY" == "darwin" ]]; then
      echo "On macOS, please install Docker Desktop (preferred) or use Homebrew with Colima:"
      echo "  brew install --cask docker    # then open the Docker app"
      echo "  # Headless alternative:"
      echo "  brew install docker docker-compose colima && colima start"
      if $INSTALL_DEPS; then
        if prompt_yes_no "Attempt to install CLI-based alternative (brew+colima)?"; then
          if command -v brew >/dev/null 2>&1; then
            brew install docker docker-compose colima && colima start || true
          else
            echo "Homebrew not found. Install from https://brew.sh then re-run." >&2
          fi
        fi
      fi
    else
      if $INSTALL_DEPS && prompt_yes_no "Install Docker Engine for Linux now?"; then
        install_docker_engine_linux "$OS_FAMILY"
        sudo usermod -aG docker "$USER" || true
        ensure_docker_running
        echo "If this is your first Docker install, you may need to log out and back in for docker group changes to take effect."
      else
        echo "Install Docker first. For Debian/Ubuntu: 'sudo apt-get install -y docker.io'" >&2
      fi
    fi
  else
    ensure_docker_running
  fi

  # Detect compose command preference: v2 plugin > v1 binary
  if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    COMPOSE="docker compose"
  elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE="docker-compose"
  else
    echo "Docker Compose not found."
    if [[ "$OS_FAMILY" == "darwin" ]]; then
      echo "On macOS, Docker Desktop includes Compose. Install Docker Desktop, or:"
      echo "  brew install docker-compose"
    else
      if $INSTALL_DEPS && prompt_yes_no "Install Docker Compose v2 plugin now?"; then
        install_compose_linux_plugin "$OS_FAMILY"
      else
        case "$OS_FAMILY" in
          amazon)
            echo "For Amazon Linux 2023: 'sudo dnf install -y docker docker-compose-plugin'" >&2
            echo "If plugin not found, download v2 plugin to /usr/local/lib/docker/cli-plugins as fallback." >&2
            ;;
          debian)
            echo "For Debian/Ubuntu: 'sudo apt-get install -y docker-compose-plugin'" >&2
            ;;
          rhel)
            echo "For RHEL/CentOS/Fedora: install 'docker' and 'docker-compose-plugin' via dnf/yum or Docker CE repo." >&2
            ;;
          *)
            echo "Install Docker Compose v2 plugin appropriate for your distro, or download the binary from GitHub releases." >&2
            ;;
        esac
      fi
      # Try detect again after attempted install
      if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
        COMPOSE="docker compose"
      elif command -v docker-compose >/dev/null 2>&1; then
        COMPOSE="docker-compose"
      else
        # Final attempt: for Linux, try binary download if allowed
        if $INSTALL_DEPS && [[ "$OS_FAMILY" != "darwin" ]]; then
          download_compose_plugin_binary
          if docker compose version >/dev/null 2>&1; then
            COMPOSE="docker compose"
          fi
        fi
        if [[ -z "${COMPOSE:-}" ]]; then
          echo "Docker Compose is still unavailable. Aborting." >&2
          exit 1
        fi
      fi
    fi
  fi
  # Final guard: ensure COMPOSE is set
  if [[ -z "${COMPOSE:-}" ]]; then
    echo "Docker Compose not available. Install Docker Desktop (macOS) or compose v2 plugin." >&2
    exit 1
  fi
}

ensure_docker_and_compose

# If GPU requested, try to ensure host GPU runtime is installed/configured
ensure_gpu_runtime

# Ensure we are in backend dir
if [[ ! -f docker-compose.yml ]]; then
  echo "Run this script from the story_gen_django directory." >&2
  exit 1
fi

# Compose files set
COMPOSE_FILES=(-f docker-compose.yml)
GPU_STATUS="disabled"
if $WITH_GPU; then
  if [[ -f docker-compose.gpu.yml ]]; then
    # Auto-skip GPU if runtime not available
    if command -v nvidia-smi >/dev/null 2>&1; then
      COMPOSE_FILES+=( -f docker-compose.gpu.yml )
      GPU_STATUS="enabled"
    else
      echo "GPU flag set but NVIDIA driver/runtime not detected (nvidia-smi missing); skipping GPU override." >&2
      GPU_STATUS="requested-missing-runtime"
    fi
  else
    echo "GPU flag set but docker-compose.gpu.yml not found; continuing without GPU override." >&2
    GPU_STATUS="requested-missing-file"
  fi
fi

# Ensure .env exists
if [[ ! -f .env ]]; then
  if [[ -f .env.example ]]; then
    cp .env.example .env
    echo "Created .env from .env.example"
  else
    cat > .env <<EOF
SECRET_KEY=$(openssl rand -hex 16)
DEBUG=True
ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1

DB_NAME=story_gen_django
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF
    echo "Created basic .env"
  fi
fi

# Ensure critical env defaults exist for runtime (avoid build-time secrets)
if ! grep -q "^OPENAI_API_KEY=" .env; then
  echo "OPENAI_API_KEY=changeme" >> .env
  echo "Added placeholder OPENAI_API_KEY to .env (update with your real key)."
fi

# Ensure DB IPv4/SSL sane defaults for managed DBs
ensure_db_ipv4_ssl

# If we generated an override file and the user requested it, include it
if $WRITE_OVERRIDE && [[ -f docker-compose.override.yml ]]; then
  COMPOSE_FILES+=( -f docker-compose.override.yml )
fi

if $CHECK_ONLY; then
  echo "Preflight completed. Exiting due to --check flag."
  exit 0
fi

##############################################
# Decide whether to use local DB/Redis services
##############################################

# Read DB_HOST and REDIS_URL from .env (fallback defaults)
DB_HOST_VAL=$(grep -E '^DB_HOST=' .env | head -n1 | cut -d'=' -f2- || true)
DB_HOST_VAL=${DB_HOST_VAL:-db}
REDIS_URL_VAL=$(grep -E '^REDIS_URL=' .env | head -n1 | cut -d'=' -f2- || true)
REDIS_URL_VAL=${REDIS_URL_VAL:-redis://redis:6379/1}

USE_LOCAL_DB=true
USE_LOCAL_REDIS=true
if [[ "$DB_HOST_VAL" != "db" && "$DB_HOST_VAL" != "localhost" && "$DB_HOST_VAL" != "127.0.0.1" ]]; then
  USE_LOCAL_DB=false
fi
if [[ ! "$REDIS_URL_VAL" =~ ^redis://redis: ]]; then
  USE_LOCAL_REDIS=false
fi

# If REDIS_URL points to 127.0.0.1, ensure local redis starts so host-network web can reach it
if [[ "$REDIS_URL_VAL" =~ ^redis://127\.0\.0\.1: ]]; then
  USE_LOCAL_REDIS=true
fi

# Allow forcing local services regardless of env
if $WITH_LOCAL_DB; then USE_LOCAL_DB=true; fi
if $WITH_LOCAL_REDIS; then USE_LOCAL_REDIS=true; fi

###############################
# Auto-configuration (DLAMI optimization, IPv6)
###############################
echo ""
echo "======================================"
echo "Auto-Configuring Environment"
echo "======================================"

# Detect and configure DLAMI ephemeral storage
detect_and_configure_dlami_storage

# Detect and configure IPv6 if needed
detect_and_configure_ipv6

echo "======================================"
echo "Auto-Configuration Complete"
echo "======================================"
echo ""

# Clean up existing containers and networks to ensure fresh state
# This prevents conflicts when network configuration changes (e.g., IPv6 enablement)
echo "Cleaning up existing containers and networks..."
$COMPOSE "${COMPOSE_FILES[@]}" down 2>/dev/null || true

# Force remove the story_gen_default network if it still exists (handles stale networks)
if docker network inspect story_gen_default >/dev/null 2>&1; then
  echo "Removing stale story_gen_default network..."
  docker network rm story_gen_default 2>/dev/null || true
fi

echo "Cleanup complete."
echo ""

# Ensure local models dir exists for persistence
mkdir -p models

if $USE_LOCAL_DB || $USE_LOCAL_REDIS; then
  echo "Bringing up local dependencies..."
  set +e
  SRVS=()
  $USE_LOCAL_DB && SRVS+=(db)
  $USE_LOCAL_REDIS && SRVS+=(redis)
  set -e
  if ((${#SRVS[@]})); then
    $COMPOSE "${COMPOSE_FILES[@]}" up -d --build "${SRVS[@]}"
  fi
fi

echo "Bringing up web..."
NO_DEPS=()
if ! $USE_LOCAL_DB && ! $USE_LOCAL_REDIS; then
  NO_DEPS=(--no-deps)
fi
$COMPOSE "${COMPOSE_FILES[@]}" up -d --build "${NO_DEPS[@]}" web

echo "Applying migrations (with retries)..."
retry 10 5 $COMPOSE "${COMPOSE_FILES[@]}" exec -T web python manage.py migrate

echo "Collecting static files (with retries)..."
retry 5 3 $COMPOSE "${COMPOSE_FILES[@]}" exec -T web python manage.py collectstatic --noinput || {
  echo "collectstatic failed. Ensure required env vars (e.g., OPENAI_API_KEY) are set in .env or environment." >&2
  exit 1
}

# Grab web container id for docker cp
WEB_CID=$($COMPOSE "${COMPOSE_FILES[@]}" ps -q web)
if [[ -z "$WEB_CID" ]]; then
  echo "Failed to resolve web container id." >&2
  exit 1
fi

echo "Setting up JoyCaption2 dependencies inside container..."
# System libs needed by OpenCV and ffmpeg; add WebP support for Pillow when available
$COMPOSE "${COMPOSE_FILES[@]}" exec -T web bash -lc "apt-get update && apt-get install -y --no-install-recommends libgl1 ffmpeg && rm -rf /var/lib/apt/lists/*"
# Best-effort install of WebP runtime (package name varies across Debian versions)
$COMPOSE "${COMPOSE_FILES[@]}" exec -T web bash -lc "apt-get update && (apt-get install -y --no-install-recommends libwebp7 || apt-get install -y --no-install-recommends libwebp6 || apt-get install -y --no-install-recommends libwebp || true) && rm -rf /var/lib/apt/lists/*"

# Python libs for JoyCaption2
$COMPOSE "${COMPOSE_FILES[@]}" exec -T web pip install --no-cache-dir transformers huggingface_hub pillow accelerate

# Install CUDA-enabled torch by default (CUDA 12.1). Fallback to CPU torch if not available.
$COMPOSE "${COMPOSE_FILES[@]}" exec -T web bash -lc "pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu121 torch || pip install --no-cache-dir torch"

# Quick torch/CUDA check
$COMPOSE "${COMPOSE_FILES[@]}" exec -T web bash -lc "python - <<'PY'
import torch
print('Torch version:', getattr(torch, '__version__', 'unknown'))
print('CUDA available:', torch.cuda.is_available())
print('Device:', (torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu'))
PY"

# Copy TripleX into container at /TripleX so backend can import it
# TripleX is optional; captioning uses HF models directly now. Preserve copy if present.
if ! $COMPOSE "${COMPOSE_FILES[@]}" exec -T web test -d /TripleX; then
  if [[ -d "../TripleX" ]]; then
    echo "Copying TripleX into container (optional)..."
    docker cp ../TripleX "$WEB_CID:/TripleX"
  else
    echo "NOTE: ../TripleX not found; proceeding with Hugging Face model captioning." >&2
  fi
fi

echo "Verifying GPU visibility in container (optional)..."
if $COMPOSE "${COMPOSE_FILES[@]}" exec -T web bash -lc "command -v nvidia-smi" >/dev/null 2>&1; then
  $COMPOSE "${COMPOSE_FILES[@]}" exec -T web nvidia-smi || true
else
  echo "nvidia-smi not found in container. If GPU is required, ensure NVIDIA runtime is configured." >&2
fi

IP=$(hostname -I 2>/dev/null | awk '{print $1}')
API_URL="http://${IP:-<remote-ip>}:8000"
echo "Backend is up. API: $API_URL"
echo "Swagger: $API_URL/api/docs/"

# Summary
DB_HOST_SUM=$(grep -E '^DB_HOST=' .env | head -n1 | cut -d'=' -f2- || echo "")
DB_HOSTADDR_SUM=$(grep -E '^DB_HOSTADDR=' .env | head -n1 | cut -d'=' -f2- || echo "")
DB_SSLMODE_SUM=$(grep -E '^DB_SSLMODE=' .env | head -n1 | cut -d'=' -f2- || echo "")
echo "Summary:"
echo "- DB host: ${DB_HOST_SUM:-db}  hostaddr: ${DB_HOSTADDR_SUM:-<none>}  sslmode: ${DB_SSLMODE_SUM:-<unset>}"
echo "- GPU: ${GPU_STATUS}"
