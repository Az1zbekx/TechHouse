// Contact page functionality

document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contact-form');
    const formSuccess = document.getElementById('form-success');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            // Get form data
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                subject: document.getElementById('subject').value,
                message: document.getElementById('message').value
            };

            // Simulate form submission
            console.log('Form submitted:', formData);

            // Hide form, show success message
            contactForm.style.display = 'none';
            formSuccess.style.display = 'block';

            // Reset form
            contactForm.reset();
        });
    }

    // Mobile menu
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const nav = document.querySelector('.nav');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
        });
    }
});
