document.addEventListener('DOMContentLoaded', () => {
    // --- Username Validation ---
    const usernameInput = document.getElementById('id_username');
    if (usernameInput) {
        const validationMessage = document.getElementById('username-validation-message');
        const validationUrl = '/ajax/validate-username/';

        usernameInput.addEventListener('input', (e) => {
            const username = e.target.value;

            if (username.length > 2) {
                fetch(`${validationUrl}?username=${username}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.is_taken) {
                            validationMessage.textContent = 'Username is already taken.';
                            validationMessage.className = 'validation-message taken';
                        } else {
                            validationMessage.textContent = 'Username is available!';
                            validationMessage.className = 'validation-message available';
                        }
                    });
            } else {
                validationMessage.textContent = '';
                validationMessage.className = 'validation-message';
            }
        });
    }

    // --- Email Validation ---
    const emailInput = document.getElementById('id_email');
    if (emailInput) {
        const emailValidationMessage = document.getElementById('email-validation-message');
        const emailValidationUrl = '/ajax/validate-email/';
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        emailInput.addEventListener('input', (e) => {
            const email = e.target.value;

            if (emailRegex.test(email)) {
                fetch(`${emailValidationUrl}?email=${email}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.is_taken) {
                            emailValidationMessage.textContent = 'This email is already registered.';
                            emailValidationMessage.className = 'validation-message taken';
                        } else {
                            emailValidationMessage.textContent = 'Email is available.';
                            emailValidationMessage.className = 'validation-message available';
                        }
                    });
            } else {
                emailValidationMessage.textContent = email.length > 0 ? 'Please enter a valid email.' : '';
                emailValidationMessage.className = 'validation-message taken';
            }
        });
    }
});