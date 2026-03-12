/* ═══════════════════════════════════════════════════════════════════════════
   IntlQ — Client-side JavaScript
   Shared utilities across all pages
   ═══════════════════════════════════════════════════════════════════════════ */

/**
 * Show a toast notification.
 * @param {string} message - The message to display.
 * @param {string} type - 'error' | 'success' | 'info'
 * @param {number} duration - Auto-dismiss duration in ms.
 */
function showToast(message, type = 'info', duration = 4000) {
    // Remove existing toasts
    document.querySelectorAll('.toast').forEach(t => t.remove());

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Format a date string.
 * @param {string} isoString - ISO date string.
 * @returns {string} Formatted date.
 */
function formatDate(isoString) {
    if (!isoString) return 'N/A';
    const d = new Date(isoString);
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

/**
 * Get a color for a score value.
 * @param {number} score - Score 0–100.
 * @returns {string} CSS color.
 */
function getScoreColor(score) {
    if (score >= 80) return 'var(--accent-green)';
    if (score >= 60) return 'var(--accent-secondary)';
    if (score >= 40) return 'var(--accent-amber)';
    return 'var(--accent-red)';
}
