/**
 * Canvas Approval Extension - Content Script
 * Simple implementation: reads static data-canvas-id attribute, shows approval UI.
 * No timing issues because canvas IDs are baked into HTML at generation time.
 */

// Configuration
const API_BASE = 'http://localhost:8000/api/v1/dev';
const HEADER_CLASS = 'canvas-approval-header';

/**
 * Initialize the extension
 */
function init() {
    console.log('[Canvas Approval] Extension loaded');

    // Check immediately
    checkForReviewPage();

    // Watch for SugarCube navigation using MutationObserver
    // (jQuery may not be loaded yet when extension initializes)
    const observer = new MutationObserver(() => {
        checkForReviewPage();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    console.log('[Canvas Approval] MutationObserver started');
}

/**
 * Check if we're on a canvas review detail page and add approval UI
 */
function checkForReviewPage() {
    const detailEl = document.getElementById('canvas-review-detail');

    // Skip if not on detail page or header already exists
    if (!detailEl || detailEl.querySelector('.' + HEADER_CLASS)) {
        return;
    }

    // Read static attributes (baked in at generation time - always available)
    const canvasId = detailEl.dataset.canvasId;
    const gameName = detailEl.dataset.gameName;

    if (canvasId && gameName) {
        console.log('[Canvas Approval] Found review page:', canvasId, 'Game:', gameName);
        addApprovalHeader(detailEl, canvasId, gameName);
    }
}

/**
 * Add approval header to the detail page
 */
function addApprovalHeader(detailEl, canvasId, gameName) {
    const header = document.createElement('div');
    header.className = HEADER_CLASS;

    header.innerHTML = `
        <div class="cap-row">
            <span class="cap-status-badge not_reviewed">Not Reviewed</span>
            <span class="cap-game-label">Game: <strong>${gameName}</strong> | Canvas: <strong>${canvasId}</strong></span>
        </div>
        <div class="cap-row">
            <button class="cap-btn cap-approve">✓ Approve</button>
            <button class="cap-btn cap-reject">✗ Needs Changes</button>
            <input type="text" class="cap-notes" placeholder="Notes..." />
        </div>
        <div class="cap-message"></div>
    `;

    // Insert at the top of the detail element
    detailEl.insertBefore(header, detailEl.firstChild);

    // Setup event listeners with toggle behavior
    header.querySelector('.cap-approve').addEventListener('click', () => {
        const currentStatus = header.dataset.currentStatus || 'not_reviewed';
        const newStatus = (currentStatus === 'approved') ? 'not_reviewed' : 'approved';
        submitApproval(gameName, canvasId, newStatus, header);
    });

    header.querySelector('.cap-reject').addEventListener('click', () => {
        const currentStatus = header.dataset.currentStatus || 'not_reviewed';
        const newStatus = (currentStatus === 'needs_changes') ? 'not_reviewed' : 'needs_changes';
        submitApproval(gameName, canvasId, newStatus, header);
    });

    console.log('[Canvas Approval] Header added for canvas:', canvasId);

    // Fetch current status from API
    fetchCurrentStatus(gameName, canvasId, header);
}

/**
 * Submit approval to backend
 */
async function submitApproval(gameName, canvasId, status, headerEl) {
    const notes = headerEl.querySelector('.cap-notes').value;

    // Disable buttons
    const buttons = headerEl.querySelectorAll('.cap-btn');
    buttons.forEach(btn => btn.disabled = true);
    showMessage(headerEl, 'Saving...', 'info');

    try {
        const response = await fetch(`${API_BASE}/canvas-approval/update`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                game: gameName,
                canvas_id: canvasId,
                status: status,
                notes: notes
            })
        });

        const data = await response.json();

        if (data.success) {
            // Update stored status
            headerEl.dataset.currentStatus = status;
            // Update badge display
            updateBadge(headerEl, status);

            const msg = status === 'approved' ? 'Approved!'
                      : status === 'needs_changes' ? 'Marked for changes'
                      : 'Reset to not reviewed';
            showMessage(headerEl, msg, 'success');
        } else {
            showMessage(headerEl, data.error || 'Failed to save', 'error');
        }
    } catch (e) {
        showMessage(headerEl, 'Error: ' + e.message, 'error');
    } finally {
        buttons.forEach(btn => btn.disabled = false);
    }
}

/**
 * Show message in header
 */
function showMessage(headerEl, message, type) {
    const msgEl = headerEl.querySelector('.cap-message');
    msgEl.textContent = message;
    msgEl.className = 'cap-message ' + type;

    if (type === 'success' || type === 'info') {
        setTimeout(() => {
            msgEl.textContent = '';
            msgEl.className = 'cap-message';
        }, 3000);
    }
}

/**
 * Format status for display
 */
function formatStatus(status) {
    switch (status) {
        case 'approved': return 'Approved';
        case 'needs_changes': return 'Needs Changes';
        default: return 'Not Reviewed';
    }
}

/**
 * Fetch current approval status from API
 */
async function fetchCurrentStatus(gameName, canvasId, headerEl) {
    try {
        const response = await fetch(
            `${API_BASE}/canvas-approval?game=${encodeURIComponent(gameName)}&canvas_id=${encodeURIComponent(canvasId)}`
        );
        const data = await response.json();

        if (data.success) {
            const status = data.status || 'not_reviewed';
            // Store current status on the header element
            headerEl.dataset.currentStatus = status;
            // Update badge display
            updateBadge(headerEl, status);
        }
    } catch (e) {
        console.log('[Canvas Approval] Could not fetch status:', e.message);
    }
}

/**
 * Update badge display
 */
function updateBadge(headerEl, status) {
    const badge = headerEl.querySelector('.cap-status-badge');
    badge.className = 'cap-status-badge ' + status;
    badge.textContent = formatStatus(status);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
