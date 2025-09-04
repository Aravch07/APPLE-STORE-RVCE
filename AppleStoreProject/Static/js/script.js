// Simple JavaScript for Apple Store RVCE

document.addEventListener('DOMContentLoaded', function() {
    console.log('Apple Store RVCE loaded successfully! 🍎');
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Add smooth transitions to product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Confirm before deleting products
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this product?')) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Confirm before removing from cart
    const removeButtons = document.querySelectorAll('.btn-remove');
    removeButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Remove this item from your cart?')) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Confirm before purchase
    const purchaseButtons = document.querySelectorAll('.btn-purchase');
    purchaseButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Complete your purchase? This action cannot be undone.')) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Simple cart animation
    const cartButtons = document.querySelectorAll('.btn-cart');
    cartButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Simple visual feedback
            const originalText = this.textContent;
            this.textContent = 'Added!';
            this.style.background = '#28a745';
            
            setTimeout(() => {
                this.textContent = originalText;
                this.style.background = '';
            }, 1500);
        });
    });
    
    // Validate quantity inputs
    const qtyInputs = document.querySelectorAll('.qty-input');
    qtyInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const min = parseInt(this.min) || 1;
            const max = parseInt(this.max) || 999;
            let value = parseInt(this.value);
            
            if (value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
                alert(`Maximum quantity available: ${max}`);
            }
        });
    });
});

// Function to toggle add product form
function toggleAddForm() {
    const form = document.getElementById('addProductForm');
    if (form) {
        if (form.style.display === 'none' || form.style.display === '') {
            form.style.display = 'block';
            form.scrollIntoView({ behavior: 'smooth' });
        } else {
            form.style.display = 'none';
        }
    }
}

// Simple loading animation for forms
function showLoading(button) {
    const originalText = button.textContent;
    button.textContent = 'Loading...';
    button.disabled = true;
    
    // Re-enable after 3 seconds (fallback)
    setTimeout(function() {
        button.textContent = originalText;
        button.disabled = false;
    }, 3000);
}

// Add loading to form submissions
document.addEventListener('submit', function(e) {
    const submitButton = e.target.querySelector('button[type="submit"]');
    if (submitButton) {
        showLoading(submitButton);
    }
});

// Simple search functionality (if needed)
function filterTable(searchTerm) {
    const table = document.querySelector('.products-table tbody');
    if (!table) return;
    
    const rows = table.querySelectorAll('tr');
    rows.forEach(function(row) {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm.toLowerCase())) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Alt + H = Home
    if (e.altKey && e.key === 'h') {
        window.location.href = '/';
    }
    
    // Alt + C = Cart
    if (e.altKey && e.key === 'c') {
        window.location.href = '/cart';
    }
    
    // Alt + P = Purchases
    if (e.altKey && e.key === 'p') {
        window.location.href = '/purchases';
    }
});

// Simple responsive menu toggle (for future mobile improvements)
function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        navLinks.classList.toggle('mobile-active');
    }
}