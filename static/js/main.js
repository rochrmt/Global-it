// Custom JavaScript for GLOBALT-IT

document.addEventListener('DOMContentLoaded', function() {
    // Back to Top Button
    const backToTopButton = document.getElementById('backToTop');
    
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.style.display = 'block';
            } else {
                backToTopButton.style.display = 'none';
            }
        });
        
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Form Validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Smooth Scrolling for Navigation Links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Counter Animation for Stats
    const counters = document.querySelectorAll('.stat-item h3');
    const animateCounter = (counter) => {
        const target = parseInt(counter.textContent.replace(/\D/g, ''));
        const increment = target / 200;
        let current = 0;
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.ceil(current) + (counter.textContent.includes('+') ? '+' : '');
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target + (counter.textContent.includes('+') ? '+' : '');
            }
        };
        
        updateCounter();
    };
    
    // Intersection Observer for Counter Animation
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = entry.target.querySelectorAll('.stat-item h3');
                counters.forEach(counter => {
                    if (!counter.classList.contains('animated')) {
                        counter.classList.add('animated');
                        animateCounter(counter);
                    }
                });
            }
        });
    }, observerOptions);
    
    const statsSection = document.querySelector('.bg-dark');
    if (statsSection) {
        observer.observe(statsSection);
    }
    
    // Service Card Hover Effect
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Formation Card Hover Effect
    const formationCards = document.querySelectorAll('.formation-card');
    formationCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Loading State for Forms
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                this.innerHTML = '<span class="loading me-2"></span>Envoi en cours...';
                this.disabled = true;
                
                // Re-enable button after 3 seconds (in case of error)
                setTimeout(() => {
                    this.disabled = false;
                    this.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Envoyer';
                }, 3000);
            }
        });
    });
    
    // Filter Formations
    const formationFilters = document.querySelectorAll('select[name="categorie"], select[name="niveau"]');
    formationFilters.forEach(filter => {
        filter.addEventListener('change', function() {
            this.form.submit();
        });
    });
    
    // Mobile Menu Toggle Animation
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    }
    
    // Add fade-in animation to elements when they come into view
    const fadeElements = document.querySelectorAll('.service-card, .formation-card, .team-card, .value-card');
    
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    fadeElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        fadeObserver.observe(element);
    });
    
    // Add active class to navigation based on current page
    const currentPath = window.location.pathname;
    const navbarLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navbarLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === '/' && currentPath === '/') {
            link.classList.add('active');
        } else if (linkPath !== '/' && currentPath.includes(linkPath)) {
            link.classList.add('active');
        }
    });
    
    // Print functionality for service and formation details
    const printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            window.print();
        });
    });
    
    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    // Show success message
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check me-1"></i>Copié!';
                    this.classList.remove('btn-outline-primary');
                    this.classList.add('btn-success');
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('btn-success');
                        this.classList.add('btn-outline-primary');
                    }, 2000);
                });
            }
        });
    });
    
    // Hero Carousel Enhancement
    const heroCarousel = document.getElementById('heroMiniCarousel');
    if (heroCarousel) {
        // Pause carousel on hover
        heroCarousel.addEventListener('mouseenter', function() {
            const carousel = bootstrap.Carousel.getInstance(this);
            if (carousel) {
                carousel.pause();
            }
        });
        
        // Resume carousel on mouse leave
        heroCarousel.addEventListener('mouseleave', function() {
            const carousel = bootstrap.Carousel.getInstance(this);
            if (carousel) {
                carousel.cycle();
            }
        });
        
        // Enhanced touch/swipe support for mobile
        let touchStartX = 0;
        let touchEndX = 0;
        
        heroCarousel.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        });
        
        heroCarousel.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        });
        
        function handleSwipe() {
            const carousel = bootstrap.Carousel.getInstance(heroCarousel);
            if (carousel) {
                if (touchEndX < touchStartX - 50) {
                    carousel.next();
                }
                if (touchEndX > touchStartX + 50) {
                    carousel.prev();
                }
            }
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft') {
                const carousel = bootstrap.Carousel.getInstance(heroCarousel);
                if (carousel) carousel.prev();
            } else if (e.key === 'ArrowRight') {
                const carousel = bootstrap.Carousel.getInstance(heroCarousel);
                if (carousel) carousel.next();
            }
        });
    }
    
    console.log('GLOBALT-IT website loaded successfully!');
});

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Error handling for images
function handleImageError(img) {
    img.onerror = null;
    img.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="%23f8f9fa"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%236c757d" font-family="Arial, sans-serif" font-size="16">Image non disponible</text></svg>';
}

// Add error handlers to images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            handleImageError(this);
        });
    });
});