/**
 * Find-Media Options Capture - Content Script
 * Injects a capture button on images/videos; clicking it stores the media URL as
 * an OPTION for the active slot (set via _tmc_game/_tmc_scene URL params by the
 * Find-media page). No download here — the find page downloads the chosen option.
 */

// Configuration
const API_ENDPOINT = 'http://localhost:8000/api/v1/dev/media-finder/options/add';
const MIN_SIZE = 50; // Minimum dimension in pixels to show button
const PROCESSED_ATTR = 'data-twine-capture';

// URL parameter names for game context
const PARAM_GAME = '_tmc_game';
const PARAM_SCENE = '_tmc_scene';

// Track active form to close it when clicking elsewhere
let activeForm = null;

// Current game context (loaded from storage)
let currentGame = null;
let currentScene = null;

/**
 * Initialize the extension
 */
async function init() {
    console.log('[Twine Media Capture] Extension loaded');

    // Check URL for game context parameters
    await checkUrlParams();

    // Load stored context
    await loadStoredContext();

    console.log('[Twine Media Capture] Context:', { game: currentGame, scene: currentScene });

    scanForMedia();
    observeDOMChanges();

    // Close form when clicking outside
    document.addEventListener('click', (e) => {
        if (activeForm && !activeForm.contains(e.target) && !e.target.closest('.twine-capture-btn')) {
            closeActiveForm();
        }
    });
}

/**
 * Check URL for game context parameters and store them
 */
async function checkUrlParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const game = urlParams.get(PARAM_GAME);
    const scene = urlParams.get(PARAM_SCENE);

    if (game || scene) {
        const context = {};
        if (game) context.currentGame = game;
        if (scene) context.currentScene = scene;

        // Store in chrome.storage.local
        await chrome.storage.local.set(context);
        console.log('[Twine Media Capture] Updated context from URL:', context);
    }
}

/**
 * Load stored context from chrome.storage.local
 */
async function loadStoredContext() {
    try {
        const data = await chrome.storage.local.get(['currentGame', 'currentScene']);
        currentGame = data.currentGame || null;
        currentScene = data.currentScene || null;
    } catch (e) {
        console.warn('[Twine Media Capture] Failed to load stored context:', e);
    }
}

/**
 * Scan page for media elements and add overlays
 */
function scanForMedia() {
    // Find all images
    document.querySelectorAll('img').forEach(addOverlayToElement);

    // Find all videos
    document.querySelectorAll('video').forEach(addOverlayToElement);
}

/**
 * Add capture overlay to a media element
 */
function addOverlayToElement(element) {
    // Skip if already processed
    if (element.hasAttribute(PROCESSED_ATTR)) return;

    // Skip tiny images (icons, etc.)
    if (element.tagName === 'IMG') {
        const width = element.naturalWidth || element.width;
        const height = element.naturalHeight || element.height;
        if (width < MIN_SIZE || height < MIN_SIZE) return;
    }

    // Skip if no valid URL
    const mediaUrl = getMediaUrl(element);
    if (!mediaUrl || mediaUrl.startsWith('data:')) return;

    // Mark as processed
    element.setAttribute(PROCESSED_ATTR, 'true');

    // Create wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'twine-capture-wrapper';

    // Copy the element's display style
    const computedStyle = window.getComputedStyle(element);
    if (computedStyle.display === 'inline') {
        wrapper.style.display = 'inline-block';
    } else {
        wrapper.style.display = computedStyle.display;
    }

    // Insert wrapper
    element.parentNode.insertBefore(wrapper, element);
    wrapper.appendChild(element);

    // Create capture button
    const button = createCaptureButton(mediaUrl, element.tagName.toLowerCase());
    wrapper.appendChild(button);
}

/**
 * Get the actual media URL from an element
 */
function getMediaUrl(element) {
    if (element.tagName === 'IMG') {
        // Try various sources
        return element.currentSrc || element.src || element.dataset.src || element.dataset.lazySrc;
    }

    if (element.tagName === 'VIDEO') {
        // Check for source elements
        const source = element.querySelector('source');
        return element.src || (source && source.src) || element.currentSrc;
    }

    return null;
}

/**
 * Create the capture button element
 */
function createCaptureButton(mediaUrl, mediaType) {
    const button = document.createElement('button');
    button.className = 'twine-capture-btn';
    button.innerHTML = '&#11015;'; // Down arrow
    button.title = 'Capture for Twine';

    button.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        showCaptureForm(mediaUrl, mediaType, button);
    });

    return button;
}

/**
 * Show the media-type popup. The slot is already known (currentScene, from the
 * _tmc_scene URL param the Find-media page sets), so we don't ask for it — we just
 * ask what KIND of media is being moved. Clicking a type button submits.
 */
function showCaptureForm(mediaUrl, mediaType, anchorButton) {
    closeActiveForm();

    const form = document.createElement('div');
    form.className = 'twine-capture-form';
    const wrapper = anchorButton.parentElement;

    // No slot context = nothing to attach the option to.
    if (!currentScene) {
        form.innerHTML = `
            <div class="twine-capture-form-label">No target slot</div>
            <div class="twine-capture-game-context">Open this tab from the Find-media page — it sets the slot via the URL.</div>
            <div class="twine-capture-form-buttons">
                <button type="button" class="twine-capture-form-btn cancel">Close</button>
            </div>`;
        wrapper.appendChild(form);
        form.querySelector('.cancel').addEventListener('click', (e) => { e.stopPropagation(); closeActiveForm(); });
        activeForm = form;
        return;
    }

    const defaultType = mediaType === 'video' ? 'video' : 'image';
    const ctx = (currentGame ? `Game: <strong>${currentGame}</strong> · ` : '') + `Slot: <strong>${currentScene}</strong>`;
    form.innerHTML = `
        <div class="twine-capture-game-context">${ctx}</div>
        <div class="twine-capture-form-label">Move as:</div>
        <div class="twine-capture-type-row">
            <button type="button" class="twine-capture-type-btn" data-type="image">Image</button>
            <button type="button" class="twine-capture-type-btn" data-type="gif">GIF</button>
            <button type="button" class="twine-capture-type-btn" data-type="video">Video</button>
        </div>
        <div class="twine-capture-form-buttons">
            <button type="button" class="twine-capture-form-btn cancel">Cancel</button>
        </div>`;

    wrapper.appendChild(form);

    form.querySelectorAll('.twine-capture-type-btn').forEach((b) => {
        if (b.dataset.type === defaultType) b.classList.add('on');
        b.addEventListener('click', (e) => {
            e.stopPropagation();
            submitCapture(mediaUrl, b.dataset.type, form, b);
        });
    });
    form.querySelector('.cancel').addEventListener('click', (e) => { e.stopPropagation(); closeActiveForm(); });

    activeForm = form;
}

/**
 * Close the active form
 */
function closeActiveForm() {
    if (activeForm) {
        activeForm.remove();
        activeForm = null;
    }
}

/**
 * Store the captured URL as an option for the active slot (no download).
 */
async function submitCapture(url, type, formElement, typeBtn) {
    const mediaKind = type === 'video' ? 'video' : 'img';  // gif/image both render as <img>
    const buttons = formElement.querySelectorAll('.twine-capture-type-btn, .cancel');
    const originalText = typeBtn.textContent;
    typeBtn.textContent = '...';
    buttons.forEach((b) => (b.disabled = true));

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                game: currentGame,
                file: currentScene,
                url: url,
                type: type,
                media_kind: mediaKind
            })
        });

        const data = await response.json();

        if (data.ok) {
            showToast('success', data.duplicate ? 'Already in options' : `Added to options (${data.count})`);
            closeActiveForm();
        } else {
            showToast('error', data.error || 'Failed to add option');
            typeBtn.textContent = originalText;
            buttons.forEach((b) => (b.disabled = false));
        }
    } catch (err) {
        showToast('error', `Request failed: ${err.message}`);
        typeBtn.textContent = originalText;
        buttons.forEach((b) => (b.disabled = false));
    }
}

/**
 * Show toast notification
 */
function showToast(type, message) {
    // Remove existing toasts
    document.querySelectorAll('.twine-capture-toast').forEach(t => t.remove());

    const toast = document.createElement('div');
    toast.className = `twine-capture-toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/**
 * Watch for dynamically added content
 */
function observeDOMChanges() {
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType !== Node.ELEMENT_NODE) return;

                // Check if the node itself is media
                if (node.tagName === 'IMG' || node.tagName === 'VIDEO') {
                    // Delay to allow images to load
                    setTimeout(() => addOverlayToElement(node), 100);
                }

                // Check for media within the node
                if (node.querySelectorAll) {
                    node.querySelectorAll('img, video').forEach((el) => {
                        setTimeout(() => addOverlayToElement(el), 100);
                    });
                }
            });
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
