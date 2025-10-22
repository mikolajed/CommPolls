document.addEventListener('DOMContentLoaded', () => {
    const countdownContainer = document.querySelector('.countdown-container');
    if (!countdownContainer) return;

    const startTime = new Date(countdownContainer.dataset.startTime);
    const serverTimeStr = countdownContainer.dataset.serverTime; // Get server's current time
    const voteUrl = countdownContainer.dataset.voteUrl;
    const pollId = countdownContainer.dataset.pollId;

    const daysEl = document.getElementById('days');
    const hoursEl = document.getElementById('hours');
    const minutesEl = document.getElementById('minutes');
    const secondsEl = document.getElementById('seconds');

    // Calculate the initial offset between client and server time
    const clientLoadTime = new Date();
    const serverLoadTime = new Date(serverTimeStr);
    const timeOffset = clientLoadTime.getTime() - serverLoadTime.getTime(); // Milliseconds difference

    const updateCountdown = () => {
        // Adjust the client's current time by the calculated offset to match server's perspective
        const now = new Date(new Date().getTime() - timeOffset);
        const distance = startTime - now;

        if (distance <= 0) {
            clearInterval(countdownInterval);
            // Use the global SPA navigation function to load the vote page.
            // This ensures that all necessary scripts for the vote page are re-initialized.
            if (window.spaNavigate) {
                window.spaNavigate(voteUrl);
            } else {
                // Fallback to a full page reload if spaNavigate is not available
                window.location.href = voteUrl;
            }
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        daysEl.textContent = String(days).padStart(2, '0');
        hoursEl.textContent = String(hours).padStart(2, '0');
        minutesEl.textContent = String(minutes).padStart(2, '0');
        secondsEl.textContent = String(seconds).padStart(2, '0');
    };

    const countdownInterval = setInterval(updateCountdown, 1000);
    updateCountdown(); // Initial call
});