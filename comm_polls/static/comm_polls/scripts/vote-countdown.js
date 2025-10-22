document.addEventListener('DOMContentLoaded', () => {
    const countdownContainer = document.querySelector('.vote-countdown');
    if (!countdownContainer) return;
    
    const endTimeStr = countdownContainer.dataset.endTime;
    const serverTimeStr = countdownContainer.dataset.serverTime;
    const timerDisplay = document.getElementById('vote-timer-display');
    const voteButton = document.querySelector('form button[type="submit"]');

    if (!endTimeStr || !serverTimeStr || !timerDisplay) return;

    const endTime = new Date(endTimeStr);
    const serverLoadTime = new Date(serverTimeStr);
    const clientLoadTime = new Date();
    const timeOffset = clientLoadTime.getTime() - serverLoadTime.getTime();

    const updateCountdown = () => {
        // Calculate the "true" current time by adjusting for the initial offset
        const now = new Date(new Date().getTime() - timeOffset);
        const distance = endTime - now;

        if (distance <= 0) {
            clearInterval(countdownInterval);
            timerDisplay.textContent = 'Poll has ended.';
            if (voteButton) {
                // Instead of disabling, we can just hide the timer and let the backend handle validation
                countdownContainer.style.display = 'none';
            }
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        let timeLeft = '';
        if (days > 0) timeLeft += `${days}d `;
        if (hours > 0 || days > 0) timeLeft += `${String(hours).padStart(2, '0')}h `;
        timeLeft += `${String(minutes).padStart(2, '0')}m `;
        timeLeft += `${String(seconds).padStart(2, '0')}s`;
        
        timerDisplay.textContent = timeLeft;
    };

    const countdownInterval = setInterval(updateCountdown, 1000);
    updateCountdown(); // Initial call
});