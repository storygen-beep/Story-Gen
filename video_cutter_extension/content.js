/**
 * Video Cutter - Content Script
 * Adds trim functionality to video elements in local game previews.
 */

// Configuration
const API_ENDPOINT = 'http://localhost:8000/api/v1/dev/video-cut';
const PROCESSED_ATTR = 'data-video-cutter';

// Track active form
let activeForm = null;

/**
 * Initialize the extension
 */
function init() {
    console.log('[Video Cutter] Extension loaded');
    scanForVideos();
    observeDOMChanges();

    // Close form when clicking outside
    document.addEventListener('click', (e) => {
        if (activeForm && !activeForm.contains(e.target) && !e.target.closest('.video-cutter-btn')) {
            closeActiveForm();
        }
    });
}

/**
 * Scan page for video elements
 */
function scanForVideos() {
    document.querySelectorAll('video').forEach(addOverlayToVideo);
}

/**
 * Add cut overlay to a video element
 */
function addOverlayToVideo(video) {
    // Skip if already processed
    if (video.hasAttribute(PROCESSED_ATTR)) return;

    // Get video URL
    const videoUrl = getVideoUrl(video);
    if (!videoUrl) return;

    // Extract relative path (e.g., "media/assets/clips/clip_023.mp4")
    const relativePath = extractRelativePath(videoUrl);
    if (!relativePath) return;

    // Mark as processed
    video.setAttribute(PROCESSED_ATTR, 'true');

    // Create wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'video-cutter-wrapper';

    const computedStyle = window.getComputedStyle(video);
    wrapper.style.display = computedStyle.display === 'inline' ? 'inline-block' : computedStyle.display;

    // Insert wrapper
    video.parentNode.insertBefore(wrapper, video);
    wrapper.appendChild(video);

    // Create scissors button
    const button = createCutButton(video, relativePath);
    wrapper.appendChild(button);
}

/**
 * Get video URL from element
 */
function getVideoUrl(video) {
    const source = video.querySelector('source');
    return video.src || (source && source.src) || video.currentSrc;
}

/**
 * Extract relative path from video URL
 * Handles both:
 * - Local: "media/assets/clips/clip_023.mp4"
 * - Absolute: "http://localhost:8080/media/assets/clips/clip_023.mp4"
 * - R2: "https://pub-xxx.r2.dev/assets/clips/clip_023.mp4"
 */
function extractRelativePath(url) {
    // Already a relative path
    if (url.startsWith('media/')) {
        return url;
    }

    // Absolute local path (served from localhost:8080)
    if (url.includes('localhost:8080')) {
        try {
            const path = new URL(url).pathname;
            return path.startsWith('/') ? path.substring(1) : path;
        } catch (e) {
            return null;
        }
    }

    // R2 URL - extract path after domain
    if (url.includes('.r2.dev/')) {
        const match = url.match(/\.r2\.dev\/(.+)$/);
        if (match) {
            return 'media/' + match[1]; // Prepend media/ for local path
        }
    }

    // Try to extract path from any URL
    try {
        const path = new URL(url).pathname;
        const cleanPath = path.startsWith('/') ? path.substring(1) : path;
        if (cleanPath) {
            return cleanPath;
        }
    } catch (e) {
        // Not a valid URL
    }

    return null;
}

/**
 * Create the scissors button
 */
function createCutButton(video, relativePath) {
    const button = document.createElement('button');
    button.className = 'video-cutter-btn';
    button.innerHTML = '&#9986;'; // Scissors character
    button.title = 'Trim this video';

    button.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        showCutForm(video, relativePath, button);
    });

    return button;
}

/**
 * Show the trim form with start/end time inputs
 */
function showCutForm(video, relativePath, anchorButton) {
    closeActiveForm();

    const form = document.createElement('div');
    form.className = 'video-cutter-form';

    // Get current video time info for defaults
    const duration = video.duration || 0;
    const filename = relativePath.split('/').pop();

    form.innerHTML = `
        <div class="video-cutter-form-header">
            <span class="video-cutter-title">&#9986; Trim Video</span>
        </div>
        <div class="video-cutter-path">${filename}</div>
        <div class="video-cutter-duration">Duration: ${formatTime(duration)}</div>

        <div class="video-cutter-row">
            <label>Start:</label>
            <input type="text" class="video-cutter-input start-time"
                   placeholder="0:00" value="0:00" />
            <button type="button" class="video-cutter-set-btn" data-target="start">Now</button>
        </div>

        <div class="video-cutter-row">
            <label>End:</label>
            <input type="text" class="video-cutter-input end-time"
                   placeholder="${formatTime(duration)}" value="${formatTime(duration)}" />
            <button type="button" class="video-cutter-set-btn" data-target="end">Now</button>
        </div>

        <div class="video-cutter-mode">
            <label>
                <input type="checkbox" class="video-cutter-precise" />
                Precise mode (slower, frame-accurate)
            </label>
        </div>

        <div class="video-cutter-form-buttons">
            <button type="button" class="video-cutter-form-btn cancel">Cancel</button>
            <button type="button" class="video-cutter-form-btn submit">Cut</button>
        </div>
    `;

    const wrapper = anchorButton.parentElement;
    wrapper.appendChild(form);

    // Focus start time input
    const startInput = form.querySelector('.start-time');
    startInput.focus();
    startInput.select();

    // "Now" buttons - set to current video time
    form.querySelectorAll('.video-cutter-set-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const target = btn.dataset.target;
            const input = form.querySelector(`.${target}-time`);
            input.value = formatTime(video.currentTime);
        });
    });

    // Keyboard handling
    form.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            submitCut(video, relativePath, form);
        } else if (e.key === 'Escape') {
            closeActiveForm();
        }
    });

    // Button handlers
    form.querySelector('.cancel').addEventListener('click', (e) => {
        e.stopPropagation();
        closeActiveForm();
    });

    form.querySelector('.submit').addEventListener('click', (e) => {
        e.stopPropagation();
        submitCut(video, relativePath, form);
    });

    activeForm = form;
}

/**
 * Format seconds to MM:SS or HH:MM:SS
 */
function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';

    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hrs > 0) {
        return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Parse time string to seconds
 * Accepts: "1:30", "01:30", "1:30:45", "90" (seconds)
 */
function parseTime(timeStr) {
    timeStr = timeStr.trim();

    // Plain seconds
    if (/^\d+(\.\d+)?$/.test(timeStr)) {
        return parseFloat(timeStr);
    }

    // MM:SS or HH:MM:SS
    const parts = timeStr.split(':').map(p => parseFloat(p));
    if (parts.some(isNaN)) {
        return NaN;
    }

    if (parts.length === 2) {
        return parts[0] * 60 + parts[1];
    } else if (parts.length === 3) {
        return parts[0] * 3600 + parts[1] * 60 + parts[2];
    }

    return NaN;
}

/**
 * Close active form
 */
function closeActiveForm() {
    if (activeForm) {
        activeForm.remove();
        activeForm = null;
    }
}

/**
 * Submit cut request to Django backend
 */
async function submitCut(video, relativePath, formElement) {
    const startInput = formElement.querySelector('.start-time');
    const endInput = formElement.querySelector('.end-time');
    const preciseCheckbox = formElement.querySelector('.video-cutter-precise');

    const startTime = parseTime(startInput.value);
    const endTime = parseTime(endInput.value);
    const preciseMode = preciseCheckbox.checked;

    // Validation
    if (isNaN(startTime) || isNaN(endTime)) {
        showToast('error', 'Invalid time format. Use MM:SS or seconds.');
        return;
    }

    if (startTime >= endTime) {
        showToast('error', 'Start time must be before end time.');
        return;
    }

    if (startTime < 0) {
        showToast('error', 'Start time cannot be negative.');
        return;
    }

    // Show loading state
    const submitBtn = formElement.querySelector('.submit');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Cutting...';
    submitBtn.disabled = true;

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_path: relativePath,
                start_time: startTime,
                end_time: endTime,
                precise_mode: preciseMode
            })
        });

        const data = await response.json();

        if (data.success) {
            showToast('success', `Video trimmed! Duration: ${data.duration}s | Backup: ${data.backup_path.split('/').pop()}`);
            closeActiveForm();

            // Reload video to show new version (cache-busting)
            const timestamp = Date.now();
            const currentSrc = video.src || video.querySelector('source')?.src;
            if (currentSrc) {
                const newSrc = currentSrc.includes('?')
                    ? currentSrc.replace(/\?.*$/, `?t=${timestamp}`)
                    : `${currentSrc}?t=${timestamp}`;

                if (video.src) {
                    video.src = newSrc;
                } else {
                    const source = video.querySelector('source');
                    if (source) {
                        source.src = newSrc;
                    }
                }
                video.load();
            }
        } else {
            showToast('error', data.error || 'Cut failed');
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
    document.querySelectorAll('.video-cutter-toast').forEach(t => t.remove());

    const toast = document.createElement('div');
    toast.className = `video-cutter-toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

/**
 * Watch for dynamically added videos
 */
function observeDOMChanges() {
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType !== Node.ELEMENT_NODE) return;

                if (node.tagName === 'VIDEO') {
                    setTimeout(() => addOverlayToVideo(node), 100);
                }

                if (node.querySelectorAll) {
                    node.querySelectorAll('video').forEach((el) => {
                        setTimeout(() => addOverlayToVideo(el), 100);
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

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
