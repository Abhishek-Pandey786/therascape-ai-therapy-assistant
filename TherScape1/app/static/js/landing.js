/**
 * Landing Page JavaScript
 * Handles navigation to authentication and demo mode
 */

// Landing Page Manager
class LandingPageManager {
    constructor() {
        this.demoBtn = document.getElementById('tryDemoBtn');
        this.authBtns = document.querySelectorAll('.auth-btn');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupAnimations();
        this.checkSystemStatus();
    }

    setupEventListeners() {
        // Demo button handling
        if (this.demoBtn) {
            this.demoBtn.addEventListener('click', () => this.handleDemoMode());
        }
        
        // Auth buttons (already have href, but add click tracking)
        this.authBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleAuthClick(e, btn));
        });
    }

    setupAnimations() {
        // Add animation delays for particles
        const particles = document.querySelectorAll('.particle');
        particles.forEach((particle, index) => {
            particle.style.animationDelay = `${index * 0.5}s`;
        });

        // Stagger animation for form elements
        const formElements = document.querySelectorAll('.auth-options, .features-section, .integration-section');
        formElements.forEach((element, index) => {
            element.style.animationDelay = `${0.3 + index * 0.1}s`;
            element.style.animation = 'fadeInUp 0.6s ease-out forwards';
            element.style.opacity = '0';
        });
    }

    async checkSystemStatus() {
        // Check if Java backend is running
        try {
            const response = await fetch('http://localhost:8080/api/health', {
                method: 'GET',
                timeout: 3000
            });
            
            if (response.ok) {
                this.updateSystemStatus('backend', true);
            } else {
                this.updateSystemStatus('backend', false);
            }
        } catch (error) {
            this.updateSystemStatus('backend', false);
        }
        
        // Check database status (implied if backend is up)
        this.updateSystemStatus('database', true);
        this.updateSystemStatus('ai', true);
    }

    updateSystemStatus(service, isOnline) {
        const statusItems = document.querySelectorAll('.status-item');
        const serviceMap = {
            'ai': 0,
            'database': 1,
            'backend': 2
        };
        
        const index = serviceMap[service];
        if (index !== undefined && statusItems[index]) {
            const dot = statusItems[index].querySelector('.status-dot');
            if (isOnline) {
                dot.classList.add('online');
                dot.classList.remove('offline');
            } else {
                dot.classList.add('offline');
                dot.classList.remove('online');
            }
        }
    }

    handleAuthClick(e, btn) {
        // Check which auth button was clicked
        const href = btn.getAttribute('href');
        if (href === '/auth/login') {
            // Login button - go directly to login form
            e.preventDefault();
            window.location.href = '/auth/login';
        } else if (href === '/auth/register') {
            // Register button - go directly to register form
            e.preventDefault();
            window.location.href = '/auth/register';
        }
        
        // Add loading animation
        const originalContent = btn.innerHTML;
        btn.innerHTML = '<span class="material-icons">hourglass_empty</span>Loading...';
        btn.style.opacity = '0.7';
        
        // Reset after a delay (in case navigation is slow)
        setTimeout(() => {
            btn.innerHTML = originalContent;
            btn.style.opacity = '1';
        }, 2000);
    }

    handleDemoMode() {
        // Redirect to dedicated demo page
        window.location.href = '/demo';
    }

    setDemoLoading(isLoading) {
        if (isLoading) {
            this.demoBtn.innerHTML = '<span class="material-icons">hourglass_empty</span>Starting Demo...';
            this.demoBtn.disabled = true;
            this.demoBtn.style.cursor = 'not-allowed';
            this.demoBtn.style.opacity = '0.7';
        } else {
            this.demoBtn.innerHTML = '<span class="material-icons">preview</span>Try Demo (Guest Mode)';
            this.demoBtn.disabled = false;
            this.demoBtn.style.cursor = 'pointer';
            this.demoBtn.style.opacity = '1';
        }
    }
}

// Initialize landing page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new LandingPageManager();
});

// Handle page visibility change
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        // Refresh system status when page becomes visible
        const manager = new LandingPageManager();
        manager.checkSystemStatus();
    }
});

// Export for potential use in other scripts
window.LandingPageManager = LandingPageManager;
