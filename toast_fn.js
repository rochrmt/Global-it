
/**
 * Affiche une notification Toast (Bootstrap 5)
 * @param {string} message - Le message à afficher
 * @param {string} type - 'success', 'error', 'info', 'warning'
 */
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) return;

    const icon = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'info': 'info-circle',
        'warning': 'exclamation-triangle'
    }[type] || 'info-circle';

    const bgClass = {
        'success': 'text-bg-success',
        'error': 'text-bg-danger',
        'info': 'text-bg-info',
        'warning': 'text-bg-warning'
    }[type] || 'text-bg-primary';

    const toastHtml = `
        <div class="toast align-items-center ${bgClass} border-0 shadow-lg" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${icon} me-2"></i> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    const wrapper = document.createElement('div');
    wrapper.innerHTML = toastHtml;
    const toastElement = wrapper.firstElementChild;
    toastContainer.appendChild(toastElement);

    const toast = new bootstrap.Toast(toastElement, {
        delay: 5000
    });
    toast.show();

    // Supprimer l'élément du DOM après la fermeture
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}
