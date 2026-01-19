// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // File upload drag and drop
    const uploadArea = document.querySelector('.upload-area');
    if (uploadArea) {
        const fileInput = document.getElementById('images');
        
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        });
    }
    
    // Confirmation dialogs for dangerous actions
    const dangerButtons = document.querySelectorAll('.btn-danger[data-confirm]');
    dangerButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = button.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-refresh functionality
    const autoRefreshToggle = document.getElementById('auto-refresh');
    if (autoRefreshToggle) {
        let refreshInterval;
        
        autoRefreshToggle.addEventListener('change', function() {
            if (this.checked) {
                // Refresh every 30 seconds
                refreshInterval = setInterval(function() {
                    location.reload();
                }, 30000);
            } else {
                clearInterval(refreshInterval);
            }
        });
    }
    
    // Quick stats auto-update
    const statsContainer = document.querySelector('.stats-container');
    if (statsContainer) {
        setInterval(function() {
            fetch('/dashboard/api/stats/')
                .then(response => response.json())
                .then(data => {
                    // Update stats display
                    updateStatsDisplay(data);
                })
                .catch(error => console.error('Error fetching stats:', error));
        }, 60000); // Update every minute
    }
    
    // Image preview functionality
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const files = e.target.files;
            const previewContainer = document.getElementById(input.getAttribute('data-preview'));
            
            if (previewContainer && files.length > 0) {
                previewContainer.innerHTML = '';
                
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    if (file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const img = document.createElement('img');
                            img.src = e.target.result;
                            img.className = 'preview-image';
                            img.style.maxWidth = '100px';
                            img.style.maxHeight = '100px';
                            img.style.objectFit = 'cover';
                            img.style.margin = '5px';
                            img.style.borderRadius = '5px';
                            previewContainer.appendChild(img);
                        };
                        reader.readAsDataURL(file);
                    }
                }
            }
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
    
    // Search functionality
    const searchInputs = document.querySelectorAll('input[data-search-target]');
    searchInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const target = document.getElementById(input.getAttribute('data-search-target'));
            if (target) {
                searchInContainer(target, input.value);
            }
        });
    });
    
    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const text = button.getAttribute('data-copy');
            copyToClipboard(text);
            
            // Show feedback
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i> Copié!';
            setTimeout(function() {
                button.innerHTML = originalText;
            }, 2000);
        });
    });
});

// Utility functions
function updateStatsDisplay(data) {
    // Update stat numbers with animation
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(function(element) {
        const currentValue = parseInt(element.textContent);
        const newValue = data[element.getAttribute('data-stat')];
        
        if (currentValue !== newValue) {
            animateNumber(element, currentValue, newValue);
        }
    });
}

function animateNumber(element, start, end) {
    const duration = 1000;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

function searchInContainer(container, searchTerm) {
    const items = container.querySelectorAll('[data-searchable]');
    const term = searchTerm.toLowerCase();
    
    items.forEach(function(item) {
        const text = item.textContent.toLowerCase();
        if (text.includes(term)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

// Dashboard specific functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        const bsAlert = new bootstrap.Alert(notification);
        bsAlert.close();
    }, 5000);
}

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

function toggleLoading(element, show = true) {
    if (show) {
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Chargement...';
        element.disabled = true;
    } else {
        element.innerHTML = element.getAttribute('data-original-text') || element.textContent;
        element.disabled = false;
    }
}

// Export functions for use in other scripts
window.DashboardUtils = {
    showNotification,
    confirmAction,
    toggleLoading,
    updateStatsDisplay,
    animateNumber,
    validateForm,
    searchInContainer,
    copyToClipboard
};