/**
 * Twine Media Capture - Content Script
 * Injects download buttons on images and videos for easy asset capture.
 */

// Configuration
const API_ENDPOINT = 'http://localhost:8000/api/v1/dev/media-capture';
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
 * Show the scene_id input form
 */
function showCaptureForm(mediaUrl, mediaType, anchorButton) {
    // Close any existing form
    closeActiveForm();

    // Create form container
    const form = document.createElement('div');
    form.className = 'twine-capture-form';

    // Build form HTML with optional game context
    let gameContextHtml = '';
    if (currentGame) {
        gameContextHtml = `<div class="twine-capture-game-context">Game: <strong>${currentGame}</strong></div>`;
    }

    form.innerHTML = `
        ${gameContextHtml}
        <div class="twine-capture-form-label">Scene ID:</div>
        <input type="text" class="twine-capture-input" placeholder="e.g. bedroom_morning" value="${currentScene || ''}" />
        <div class="twine-capture-form-buttons">
            <button type="button" class="twine-capture-form-btn cancel">Cancel</button>
            <button type="button" class="twine-capture-form-btn submit">Save</button>
        </div>
    `;

    // Position near the button
    const wrapper = anchorButton.parentElement;
    wrapper.appendChild(form);

    // Focus input and select text if pre-filled
    const input = form.querySelector('.twine-capture-input');
    input.focus();
    if (currentScene) {
        input.select();
    }

    // Handle enter key
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            submitCapture(mediaUrl, input.value, form);
        } else if (e.key === 'Escape') {
            closeActiveForm();
        }
    });

    // Handle buttons
    form.querySelector('.cancel').addEventListener('click', (e) => {
        e.stopPropagation();
        closeActiveForm();
    });

    form.querySelector('.submit').addEventListener('click', (e) => {
        e.stopPropagation();
        submitCapture(mediaUrl, input.value, form);
    });

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
 * Submit capture request to Django backend
 */
async function submitCapture(url, sceneId, formElement) {
    // Validate
    if (!sceneId.trim()) {
        showToast('error', 'Please enter a scene ID');
        return;
    }

    // Show loading state
    const submitBtn = formElement.querySelector('.submit');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = '...';
    submitBtn.disabled = true;

    try {
        // Build request body with optional game parameter
        const requestBody = {
            url: url,
            scene_id: sceneId.trim()
        };

        // Add game if we have context
        if (currentGame) {
            requestBody.game = currentGame;
        }

        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();

        if (data.success) {
            showToast('success', `Saved: ${data.file_path}`);
            closeActiveForm();
        } else {
            showToast('error', data.error || 'Download failed');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    } catch (err) {
        showToast('error', `Request failed: ${err.message}`);
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
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
