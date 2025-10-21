document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('.password-toggle-btn');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const wrapper = button.closest('.password-input-wrapper');
            const passwordInput = wrapper.querySelector('input');
            
            if (passwordInput) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    button.textContent = '🙈';
                } else {
                    passwordInput.type = 'password';
                    button.textContent = '👁️';
                }
            }
        });
    });
});