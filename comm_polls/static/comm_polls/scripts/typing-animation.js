document.addEventListener('DOMContentLoaded', () => {
    const subtitleElement = document.getElementById('typing-subtitle');
    if (!subtitleElement) return;

    const textToType = "Create, share, and vote on polls instantly.";
    let charIndex = 0;

    // Clear initial content to ensure it's empty before typing
    subtitleElement.textContent = '';

    function type() {
        if (charIndex < textToType.length) {
            subtitleElement.textContent += textToType.charAt(charIndex);
            charIndex++;
            setTimeout(type, 50); // Adjust typing speed here (milliseconds)
        } else {
            // Typing is finished, remove the cursor
            subtitleElement.classList.add('typing-done');
        }
    }

    type();
});