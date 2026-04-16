"""
Modular Prompt Builder for Elora CLI.

Loads and combines prompt modules from organized directory structure.
Provides comprehensive context loading with proper ordering and caching.
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class PromptBuilder:
    """
    Build comprehensive prompt from modular components.

    Loads modules in logical order to create complete system context.
    Provides caching for performance and validation for consistency.
    """

    def __init__(self, base_dir: Path | str):
        self.base_dir = Path(base_dir)
        self.modules_dir = self.base_dir / "modules"

        # Define module loading order
        self.module_order = [
            "core",          # System identity and basic setup
            "foundations",   # Core concepts and hierarchy
            "technical",     # Implementation details and APIs
            "creative",      # Design and psychology principles
            "workflows",     # Processes and decision-making
            "specialized"    # Mode-specific extensions
        ]

        self._cache = {}
        self._last_scan = None

    def load_all_modules(self) -> str:
        """
        Load and combine all modules into comprehensive prompt.

        Returns:
            str: Complete system prompt combining all modules
        """
        if not self.modules_dir.exists():
            raise FileNotFoundError(f"Modules directory not found: {self.modules_dir}")

        sections = []

        # Add header
        sections.append("# Elora AI - Comprehensive System Prompt")
        sections.append("# Generated from modular prompt components")
        sections.append(f"# Built: {datetime.now().isoformat()}")
        sections.append("")

        # Load modules in defined order
        for category in self.module_order:
            category_section = self._load_category(category)
            if category_section:
                sections.append(f"# ==================== {category.upper()} ====================")
                sections.append("")
                sections.append(category_section)
                sections.append("")

        return "\n".join(sections)

    def _load_category(self, category: str) -> str:
        """
        Load all modules from a category directory.

        Args:
            category: Category name (core, foundations, technical, etc.)

        Returns:
            str: Combined content from all modules in category
        """
        category_path = self.modules_dir / category
        if not category_path.exists():
            logger.warning(f"Category directory not found: {category_path}")
            return ""

        modules = []

        # Load all .md files in category, sorted by name
        for module_file in sorted(category_path.glob("*.md")):
            try:
                content = module_file.read_text(encoding='utf-8').strip()
                if content:
                    modules.append(f"## {module_file.stem.replace('_', ' ').title()}\n\n{content}")
            except Exception as e:
                logger.error(f"Failed to load module {module_file}: {e}")
                continue

        return "\n\n".join(modules) if modules else ""

    def validate_modules(self) -> Dict[str, Any]:
        """
        Validate all modules for consistency and completeness.

        Returns:
            dict: Validation results with issues and statistics
        """
        results = {
            "valid": True,
            "issues": [],
            "statistics": {},
            "missing_modules": [],
            "empty_modules": []
        }

        total_files = 0
        total_chars = 0

        for category in self.module_order:
            category_path = self.modules_dir / category

            if not category_path.exists():
                results["issues"].append(f"Missing category directory: {category}")
                results["valid"] = False
                continue

            category_files = list(category_path.glob("*.md"))
            if not category_files:
                results["missing_modules"].append(category)
                results["issues"].append(f"No modules found in category: {category}")

            for module_file in category_files:
                total_files += 1
                try:
                    content = module_file.read_text(encoding='utf-8').strip()
                    if not content:
                        results["empty_modules"].append(str(module_file))
                        results["issues"].append(f"Empty module: {module_file}")
                    else:
                        total_chars += len(content)
                except Exception as e:
                    results["issues"].append(f"Cannot read module {module_file}: {e}")
                    results["valid"] = False

        results["statistics"] = {
            "total_files": total_files,
            "total_characters": total_chars,
            "estimated_tokens": total_chars // 4,
            "categories": len(self.module_order)
        }

        return results

    def list_modules(self) -> Dict[str, List[str]]:
        """
        List all available modules by category.

        Returns:
            dict: Mapping of category -> list of module names
        """
        modules = {}

        for category in self.module_order:
            category_path = self.modules_dir / category
            if category_path.exists():
                modules[category] = [
                    f.stem for f in sorted(category_path.glob("*.md"))
                ]
            else:
                modules[category] = []

        return modules

    def get_module_content(self, category: str, module_name: str) -> Optional[str]:
        """
        Get content of specific module.

        Args:
            category: Category name
            module_name: Module name (without .md extension)

        Returns:
            str or None: Module content if found
        """
        module_path = self.modules_dir / category / f"{module_name}.md"

        if not module_path.exists():
            return None

        try:
            return module_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to read module {module_path}: {e}")
            return None

    def reload_cache(self) -> None:
        """Clear internal cache and force reload on next access."""
        self._cache.clear()
        self._last_scan = None

    def __str__(self) -> str:
        """String representation showing module statistics."""
        try:
            validation = self.validate_modules()
            stats = validation["statistics"]
            return (f"PromptBuilder: {stats['total_files']} modules, "
                    f"{stats['estimated_tokens']:,} tokens, "
                    f"{'valid' if validation['valid'] else 'invalid'}")
        except Exception:
            return f"PromptBuilder: {self.modules_dir}"