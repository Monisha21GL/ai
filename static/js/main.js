/**
 * AI Healthcare Assistant - Main JavaScript File
 * 
 * This file contains core functionality for the healthcare assistant
 * including navigation, form handling, and UI interactions.
 */

// Global variables
let currentUser = null;
let isEmergency = false;

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('AI Healthcare Assistant - Initializing...');
    
    // Initialize navigation
    initializeNavigation();
    
    // Initialize forms
    initializeForms();
    
    // Initialize emergency system
    initializeEmergencySystem();
    
    // Initialize tooltips and help text
    initializeHelpers();
    
    // Initialize animations and interactions
    initializeAnimations();
    
    // Initialize accessibility features
    initializeAccessibility();
    
    // Initialize theme system
    initializeTheme();
    
    console.log('AI Healthcare Assistant - Ready!');
}

/**
 * Initialize navigation functionality
 */
function initializeNavigation() {
    const mobileMenu = document.getElementById('mobile-menu');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenu && navMenu) {
        mobileMenu.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
    
    // Highlight current page in navigation
    highlightCurrentPage();
}

/**
 * Highlight the current page in navigation
 */
function highlightCurrentPage() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });
}

/**
 * Initialize form functionality
 */
function initializeForms() {
    // Add form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
    
    // Add input validation
    const inputs = document.querySelectorAll('.form-input, .form-select, .form-textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', validateInput);
        input.addEventListener('input', clearValidationError);
    });
}

/**
 * Handle form submission
 */
function handleFormSubmit(event) {
    const form = event.target;
    const formData = new FormData(form);
    
    // Basic validation
    if (!validateForm(form)) {
        event.preventDefault();
        return false;
    }
    
    // Show loading state
    showLoadingState(form);
    
    // Form will submit normally, but we can add AJAX handling here if needed
    console.log('Form submitted:', form.id || form.className);
}

/**
 * Validate form inputs
 */
function validateForm(form) {
    let isValid = true;
    const requiredInputs = form.querySelectorAll('[required]');
    
    requiredInputs.forEach(input => {
        if (!validateInput({ target: input })) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Validate individual input
 */
function validateInput(event) {
    const input = event.target;
    const value = input.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // Check if required field is empty
    if (input.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    
    // Email validation
    if (input.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    }
    
    // Phone validation
    if (input.type === 'tel' && value) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
            isValid = false;
            errorMessage = 'Please enter a valid phone number';
        }
    }
    
    // Date validation (not in the past for appointments)
    if (input.type === 'date' && value && input.name === 'appointment_date') {
        const selectedDate = new Date(value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            isValid = false;
            errorMessage = 'Please select a future date';
        }
    }
    
    // Show/hide error message
    if (!isValid) {
        showInputError(input, errorMessage);
    } else {
        clearInputError(input);
    }
    
    return isValid;
}

/**
 * Show input validation error
 */
function showInputError(input, message) {
    clearInputError(input);
    
    input.classList.add('error');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'input-error';
    errorDiv.textContent = message;
    
    input.parentNode.appendChild(errorDiv);
}

/**
 * Clear input validation error
 */
function clearInputError(input) {
    input.classList.remove('error');
    
    const existingError = input.parentNode.querySelector('.input-error');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Clear validation error on input
 */
function clearValidationError(event) {
    const input = event.target;
    if (input.classList.contains('error')) {
        clearInputError(input);
    }
}

/**
 * Show loading state for forms
 */
function showLoadingState(form) {
    const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="loading"></span> Processing...';
    }
}

/**
 * Hide loading state for forms
 */
function hideLoadingState(form) {
    const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
    if (submitButton) {
        submitButton.disabled = false;
        submitButton.innerHTML = submitButton.getAttribute('data-original-text') || 'Submit';
    }
}

/**
 * Initialize emergency system
 */
function initializeEmergencySystem() {
    const dismissButton = document.getElementById('dismiss-alert');
    const callButton = document.getElementById('call-ambulance');
    
    if (dismissButton) {
        dismissButton.addEventListener('click', dismissEmergencyAlert);
    }
    
    if (callButton) {
        callButton.addEventListener('click', simulateAmbulanceCall);
    }
}

/**
 * Show emergency alert
 */
function showEmergencyAlert(message, ambulanceContact) {
    const alertElement = document.getElementById('emergency-alert');
    const messageElement = document.getElementById('emergency-message');
    
    if (alertElement && messageElement) {
        messageElement.textContent = message || 'Emergency detected! Please seek immediate medical attention.';
        alertElement.classList.remove('hidden');
        
        // Scroll to top to ensure alert is visible
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Set emergency state
        isEmergency = true;
        
        // Auto-focus on emergency actions
        const callButton = document.getElementById('call-ambulance');
        if (callButton) {
            callButton.focus();
        }
    }
}

/**
 * Dismiss emergency alert
 */
function dismissEmergencyAlert() {
    const alertElement = document.getElementById('emergency-alert');
    if (alertElement) {
        alertElement.classList.add('hidden');
        isEmergency = false;
    }
}

/**
 * Simulate ambulance call
 */
function simulateAmbulanceCall() {
    // In a real application, this would integrate with emergency services
    alert('🚨 EMERGENCY CALL SIMULATION 🚨\n\nCalling ambulance services...\nContact: 911\n\nThis is a simulation for academic purposes only.\nIn a real emergency, call your local emergency number immediately!');
    
    // Log the emergency call
    console.log('Emergency call simulated at:', new Date().toISOString());
    
    // You could also send this data to the server for logging
    logEmergencyCall();
}

/**
 * Log emergency call to server
 */
function logEmergencyCall() {
    const emergencyData = {
        timestamp: new Date().toISOString(),
        action: 'ambulance_call_simulated',
        user_session: getCurrentUserSession()
    };
    
    // Send to server (implement when backend is ready)
    console.log('Emergency call logged:', emergencyData);
}

/**
 * Get current user session ID
 */
function getCurrentUserSession() {
    // This would typically come from the server or session storage
    return sessionStorage.getItem('user_session') || 'anonymous';
}

/**
 * Initialize helper functionality
 */
function initializeHelpers() {
    // Add tooltips to help icons
    const helpIcons = document.querySelectorAll('.help-icon');
    helpIcons.forEach(icon => {
        icon.addEventListener('mouseenter', showTooltip);
        icon.addEventListener('mouseleave', hideTooltip);
    });
    
    // Add smooth scrolling to anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', smoothScroll);
    });
}

/**
 * Show tooltip
 */
function showTooltip(event) {
    const helpIcon = event.target;
    const tooltipText = helpIcon.getAttribute('data-tooltip');
    
    if (tooltipText) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = tooltipText;
        
        document.body.appendChild(tooltip);
        
        // Position tooltip
        const rect = helpIcon.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
    }
}

/**
 * Hide tooltip
 */
function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

/**
 * Smooth scroll to anchor
 */
function smoothScroll(event) {
    event.preventDefault();
    
    const targetId = event.target.getAttribute('href').substring(1);
    const targetElement = document.getElementById(targetId);
    
    if (targetElement) {
        targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Utility function to make AJAX requests
 */
function makeRequest(url, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        
        xhr.open(method, url);
        xhr.setRequestHeader('Content-Type', 'application/json');
        
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    resolve(response);
                } catch (e) {
                    resolve(xhr.responseText);
                }
            } else {
                reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`));
            }
        };
        
        xhr.onerror = function() {
            reject(new Error('Network error'));
        };
        
        if (data) {
            xhr.send(JSON.stringify(data));
        } else {
            xhr.send();
        }
    });
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add close button
    const closeButton = document.createElement('button');
    closeButton.className = 'notification-close';
    closeButton.innerHTML = '&times;';
    closeButton.addEventListener('click', () => notification.remove());
    
    notification.appendChild(closeButton);
    document.body.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

/**
 * Format date for display
 */
function formatDate(date) {
    if (!(date instanceof Date)) {
        date = new Date(date);
    }
    
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Format time for display
 */
function formatTime(time) {
    if (typeof time === 'string') {
        const [hours, minutes] = time.split(':');
        const date = new Date();
        date.setHours(parseInt(hours), parseInt(minutes));
        time = date;
    }
    
    return time.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// Export functions for use in other scripts
window.HealthcareApp = {
    showEmergencyAlert,
    dismissEmergencyAlert,
    showNotification,
    makeRequest,
    formatDate,
    formatTime,
    getCurrentUserSession
};

/**
 * Initialize animations and micro-interactions
 */
function initializeAnimations() {
    // Add stagger animation to dashboard cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add intersection observer for scroll animations
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        }, observerOptions);
        
        // Observe elements that should animate on scroll
        const animateElements = document.querySelectorAll('.results-container, .form-container');
        animateElements.forEach(el => observer.observe(el));
    }
    
    // Add ripple effect to buttons
    addRippleEffect();
    
    // Add hover effects to interactive elements
    addHoverEffects();
}

/**
 * Add ripple effect to buttons
 */
function addRippleEffect() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

/**
 * Add enhanced hover effects
 */
function addHoverEffects() {
    const cards = document.querySelectorAll('.feature-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

/**
 * Initialize accessibility features
 */
function initializeAccessibility() {
    // Add skip link
    addSkipLink();
    
    // Enhance keyboard navigation
    enhanceKeyboardNavigation();
    
    // Add ARIA labels and descriptions
    addAriaLabels();
    
    // Handle reduced motion preferences
    handleReducedMotion();
}

/**
 * Add skip link for screen readers
 */
function addSkipLink() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Skip to main content';
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Add main content ID if it doesn't exist
    const mainContent = document.querySelector('.main-content');
    if (mainContent && !mainContent.id) {
        mainContent.id = 'main-content';
    }
}

/**
 * Enhance keyboard navigation
 */
function enhanceKeyboardNavigation() {
    // Make feature cards keyboard accessible
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        if (!card.hasAttribute('tabindex')) {
            card.setAttribute('tabindex', '0');
        }
        
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const button = this.querySelector('.btn');
                if (button) {
                    button.click();
                }
            }
        });
    });
    
    // Trap focus in modals
    trapFocusInModals();
}

/**
 * Trap focus in modal dialogs
 */
function trapFocusInModals() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                const focusableElements = this.querySelectorAll(
                    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
                );
                
                const firstElement = focusableElements[0];
                const lastElement = focusableElements[focusableElements.length - 1];
                
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        e.preventDefault();
                        lastElement.focus();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        e.preventDefault();
                        firstElement.focus();
                    }
                }
            }
            
            if (e.key === 'Escape') {
                closeModal(this);
            }
        });
    });
}

/**
 * Add ARIA labels and descriptions
 */
function addAriaLabels() {
    // Add ARIA labels to form inputs without labels
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (!input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')) {
            const label = input.closest('.form-group')?.querySelector('label');
            if (label) {
                input.setAttribute('aria-labelledby', label.id || generateId('label'));
                if (!label.id) {
                    label.id = input.getAttribute('aria-labelledby');
                }
            }
        }
    });
    
    // Add ARIA descriptions to help text
    const helpTexts = document.querySelectorAll('.help-text');
    helpTexts.forEach(help => {
        const input = help.closest('.form-group')?.querySelector('input, select, textarea');
        if (input) {
            const helpId = help.id || generateId('help');
            help.id = helpId;
            input.setAttribute('aria-describedby', helpId);
        }
    });
}

/**
 * Handle reduced motion preferences
 */
function handleReducedMotion() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        // Disable animations for users who prefer reduced motion
        const style = document.createElement('style');
        style.textContent = `
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * Initialize theme system
 */
function initializeTheme() {
    // Check for saved theme preference or default to system preference
    const savedTheme = localStorage.getItem('healthcare-theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    const theme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    setTheme(theme);
    
    // Add theme toggle if it exists
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('healthcare-theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
}

/**
 * Set theme
 */
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('healthcare-theme', theme);
    
    // Update theme toggle button if it exists
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
        themeToggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
    }
}

/**
 * Toggle theme
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

/**
 * Generate unique ID
 */
function generateId(prefix = 'id') {
    return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Close modal
 */
function closeModal(modal) {
    modal.classList.remove('active');
    
    // Return focus to the element that opened the modal
    const trigger = document.querySelector(`[data-modal="${modal.id}"]`);
    if (trigger) {
        trigger.focus();
    }
}

/**
 * Enhanced notification system
 */
function showEnhancedNotification(message, type = 'info', options = {}) {
    const {
        duration = 5000,
        position = 'top-right',
        closable = true,
        actions = []
    } = options;
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} notification-${position}`;
    
    // Create notification content
    const content = document.createElement('div');
    content.className = 'notification-content';
    
    const messageEl = document.createElement('div');
    messageEl.className = 'notification-message';
    messageEl.textContent = message;
    content.appendChild(messageEl);
    
    // Add actions if provided
    if (actions.length > 0) {
        const actionsEl = document.createElement('div');
        actionsEl.className = 'notification-actions';
        
        actions.forEach(action => {
            const button = document.createElement('button');
            button.className = 'btn btn-sm';
            button.textContent = action.text;
            button.addEventListener('click', () => {
                action.handler();
                notification.remove();
            });
            actionsEl.appendChild(button);
        });
        
        content.appendChild(actionsEl);
    }
    
    notification.appendChild(content);
    
    // Add close button if closable
    if (closable) {
        const closeButton = document.createElement('button');
        closeButton.className = 'notification-close';
        closeButton.innerHTML = '&times;';
        closeButton.setAttribute('aria-label', 'Close notification');
        closeButton.addEventListener('click', () => notification.remove());
        notification.appendChild(closeButton);
    }
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Trigger entrance animation
    requestAnimationFrame(() => {
        notification.classList.add('show');
    });
    
    // Auto-remove after duration
    if (duration > 0) {
        setTimeout(() => {
            if (notification.parentNode) {
                notification.classList.remove('show');
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
    }
    
    return notification;
}

/**
 * Enhanced loading states
 */
function showLoadingOverlay(message = 'Loading...') {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading-content">
            <div class="loading-spinner"></div>
            <div class="loading-message">${message}</div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    requestAnimationFrame(() => {
        overlay.classList.add('show');
    });
    
    return overlay;
}

/**
 * Hide loading overlay
 */
function hideLoadingOverlay(overlay) {
    if (overlay && overlay.parentNode) {
        overlay.classList.remove('show');
        setTimeout(() => overlay.remove(), 300);
    }
}

// Add CSS for new components
const additionalStyles = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .notification {
        position: fixed;
        z-index: 1000;
        padding: 1rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
        min-width: 300px;
    }
    
    .notification.notification-top-right {
        top: 20px;
        right: 20px;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-content {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .notification-actions {
        display: flex;
        gap: 0.5rem;
        justify-content: flex-end;
    }
    
    .notification-close {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        background: none;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        color: inherit;
        opacity: 0.7;
    }
    
    .notification-close:hover {
        opacity: 1;
    }
    
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .loading-overlay.show {
        opacity: 1;
    }
    
    .loading-content {
        background: var(--bg-primary);
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        box-shadow: var(--shadow-lg);
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid var(--border-color);
        border-top-color: var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
`;

// Add the styles to the document
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Update the exported functions
window.HealthcareApp = {
    ...window.HealthcareApp,
    showEnhancedNotification,
    showLoadingOverlay,
    hideLoadingOverlay,
    setTheme,
    toggleTheme
};

/**
 * Theme Toggle Functionality
 */
function initializeTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Set initial theme
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeToggleIcon(currentTheme);
    
    // Theme toggle event listener
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeToggleIcon(newTheme);
            
            // Show notification
            HealthcareApp.showNotification(`Switched to ${newTheme} mode`, 'info');
        });
    }
}

/**
 * Update theme toggle icon
 */
function updateThemeToggleIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
        themeToggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    }
}

/**
 * Health Chatbot Functionality
 */
class HealthChatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.initialize();
    }
    
    initialize() {
        this.createChatbotElements();
        this.bindEvents();
    }
    
    createChatbotElements() {
        // Create chatbot toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'chatbot-toggle';
        toggleBtn.className = 'chatbot-toggle';
        toggleBtn.innerHTML = '💬';
        toggleBtn.setAttribute('aria-label', 'Open health chatbot');
        document.body.appendChild(toggleBtn);
        
        // Create chatbot container
        const container = document.createElement('div');
        container.id = 'chatbot-container';
        container.className = 'chatbot-container';
        container.innerHTML = `
            <div class="chatbot-header">
                <h4>🤖 Health Assistant</h4>
                <button class="chatbot-close" aria-label="Close chatbot">&times;</button>
            </div>
            <div class="chatbot-messages" id="chatbot-messages">
                <div class="message bot">
                    Hello! I'm your AI Health Assistant. I can help with general health questions and guide you to our healthcare features. How can I help you today?
                </div>
            </div>
            <div class="chatbot-input">
                <input type="text" id="chatbot-input" placeholder="Type your health question..." maxlength="500">
                <button class="chatbot-send" id="chatbot-send">Send</button>
            </div>
        `;
        document.body.appendChild(container);
    }
    
    bindEvents() {
        const toggleBtn = document.getElementById('chatbot-toggle');
        const closeBtn = document.querySelector('.chatbot-close');
        const sendBtn = document.getElementById('chatbot-send');
        const input = document.getElementById('chatbot-input');
        
        // Toggle chatbot
        toggleBtn.addEventListener('click', () => this.toggle());
        closeBtn.addEventListener('click', () => this.close());
        
        // Send message
        sendBtn.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            const container = document.getElementById('chatbot-container');
            if (this.isOpen && !container.contains(e.target) && !toggleBtn.contains(e.target)) {
                this.close();
            }
        });
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        const container = document.getElementById('chatbot-container');
        const toggleBtn = document.getElementById('chatbot-toggle');
        
        container.classList.add('active');
        toggleBtn.classList.add('active');
        this.isOpen = true;
        
        // Focus input
        const input = document.getElementById('chatbot-input');
        setTimeout(() => input.focus(), 100);
    }
    
    close() {
        const container = document.getElementById('chatbot-container');
        const toggleBtn = document.getElementById('chatbot-toggle');
        
        container.classList.remove('active');
        toggleBtn.classList.remove('active');
        this.isOpen = false;
    }
    
    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addMessage(message, 'user');
        input.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send to chatbot API
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator();
            
            if (data.success) {
                // Add bot response
                this.addMessage(data.response, 'bot', data.suggestions);
            } else {
                this.addMessage('Sorry, I\'m having trouble processing your request. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Chatbot error:', error);
            this.removeTypingIndicator();
            this.addMessage('I\'m temporarily unavailable. Please try again later.', 'bot');
        }
    }
    
    addMessage(text, sender, suggestions = []) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        
        // Add suggestions if provided
        if (suggestions && suggestions.length > 0) {
            const suggestionsDiv = document.createElement('div');
            suggestionsDiv.className = 'message-suggestions';
            
            suggestions.forEach(suggestion => {
                const btn = document.createElement('button');
                btn.className = 'suggestion-btn';
                btn.textContent = suggestion.text;
                btn.addEventListener('click', () => {
                    this.handleSuggestionClick(suggestion.action);
                });
                suggestionsDiv.appendChild(btn);
            });
            
            messageDiv.appendChild(suggestionsDiv);
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatbot-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.innerHTML = '<span>Typing...</span>';
        typingDiv.id = 'typing-indicator';
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    handleSuggestionClick(action) {
        switch (action) {
            case 'symptom_checker':
                window.location.href = '/symptom-checker';
                break;
            case 'emergency_check':
                window.location.href = '/check-emergency';
                break;
            case 'book_appointment':
                window.location.href = '/book-appointment';
                break;
            case 'find_hospitals':
                window.location.href = '/get-location';
                break;
            case 'health_tips':
                this.showHealthTips();
                break;
            case 'medical_history':
                window.location.href = '/medical-history';
                break;
            default:
                console.log('Unknown action:', action);
        }
    }
    
    async showHealthTips() {
        try {
            const response = await fetch('/health-tips');
            const data = await response.json();
            
            if (data.success) {
                this.displayHealthTipsModal(data.tips);
            } else {
                this.addMessage('Sorry, I couldn\'t load health tips right now.', 'bot');
            }
        } catch (error) {
            console.error('Health tips error:', error);
            this.addMessage('Sorry, I couldn\'t load health tips right now.', 'bot');
        }
    }
    
    displayHealthTipsModal(tips) {
        // Create modal
        const modal = document.createElement('div');
        modal.className = 'health-tips-modal active';
        modal.innerHTML = `
            <div class="health-tips-content">
                <div class="health-tips-header">
                    <h3>💡 Personalized Health Tips</h3>
                    <button class="btn btn-secondary" onclick="this.closest('.health-tips-modal').remove()">&times;</button>
                </div>
                <div class="health-tips-list">
                    ${tips.map(tip => `
                        <div class="health-tip-card priority-${tip.priority}">
                            <div class="tip-header">
                                <span class="tip-icon">${tip.icon}</span>
                                <span class="tip-category">${tip.category}</span>
                                <span class="tip-priority ${tip.priority}">${tip.priority}</span>
                            </div>
                            <p class="tip-content">${tip.content}</p>
                        </div>
                    `).join('')}
                </div>
                <div class="tips-footer">
                    <p><em>These tips are for informational purposes only. Always consult healthcare professionals for personalized medical advice.</em></p>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close on outside click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }
}

/**
 * Health Tips Functionality
 */
class HealthTips {
    static async getDailyTip() {
        try {
            const response = await fetch('/daily-tip');
            const data = await response.json();
            
            if (data.success) {
                return data.tip;
            }
            return null;
        } catch (error) {
            console.error('Daily tip error:', error);
            return null;
        }
    }
    
    static async searchTips(query) {
        try {
            const response = await fetch(`/search-tips?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                return data.tips;
            }
            return [];
        } catch (error) {
            console.error('Tip search error:', error);
            return [];
        }
    }
    
    static async getPersonalizedTips() {
        try {
            const response = await fetch('/health-tips');
            const data = await response.json();
            
            if (data.success) {
                return data.tips;
            }
            return [];
        } catch (error) {
            console.error('Personalized tips error:', error);
            return [];
        }
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize chatbot
    window.healthChatbot = new HealthChatbot();
    
    // Initialize health tips
    window.HealthTips = HealthTips;
    
    // Add daily tip to dashboard if present
    const dailyTipContainer = document.getElementById('daily-tip-container');
    if (dailyTipContainer) {
        HealthTips.getDailyTip().then(tip => {
            if (tip) {
                dailyTipContainer.innerHTML = `
                    <div class="daily-tip">
                        <h4>${tip.icon} ${tip.title}</h4>
                        <p>${tip.content}</p>
                        <small>Category: ${tip.category}</small>
                    </div>
                `;
            }
        });
    }
});

/**
 * Enhanced Features Integration
 */
class EnhancedFeatures {
    static initializeAll() {
        // Initialize theme toggle
        initializeTheme();
        
        // Initialize chatbot
        if (!window.healthChatbot) {
            window.healthChatbot = new HealthChatbot();
        }
        
        // Initialize health tips
        window.HealthTips = HealthTips;
        
        console.log('Enhanced features initialized');
    }
    
    static showHealthTipsModal() {
        if (window.healthChatbot) {
            window.healthChatbot.showHealthTips();
        }
    }
    
    static toggleTheme() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.click();
        }
    }
    
    static openChatbot() {
        if (window.healthChatbot) {
            window.healthChatbot.open();
        }
    }
}

// Make enhanced features available globally
window.EnhancedFeatures = EnhancedFeatures;

// Auto-initialize enhanced features
document.addEventListener('DOMContentLoaded', function() {
    EnhancedFeatures.initializeAll();
});