console.log('[Countdown] Script loaded.');

window.initCountdown = function initCountdown() {
    console.log('[Countdown] Initialization triggered.');

    // Avoid duplicate intervals
    if (window.currentCountdownInterval) {
        clearInterval(window.currentCountdownInterval);
        window.currentCountdownInterval = null;
    }

    const container = document.querySelector('.countdown-container');
    if (!container) {
        console.warn('[Countdown] Container not found. Retrying...');
        return setTimeout(initCountdown, 100); // Retry until DOM is ready
    }

    const startTimeStr = container.dataset.startTime;
    const serverTimeStr = container.dataset.serverTime;
    const voteUrl = container.dataset.voteUrl;

    if (!startTimeStr || !serverTimeStr) {
        console.error('[Countdown] Missing startTime or serverTime.');
        return;
    }

    const startTime = new Date(startTimeStr);
    const serverLoadTime = new Date(serverTimeStr);
    const clientLoadTime = new Date();
    const timeOffset = clientLoadTime.getTime() - serverLoadTime.getTime();

    const daysEl = container.querySelector('#days');
    const hoursEl = container.querySelector('#hours');
    const minutesEl = container.querySelector('#minutes');
    const secondsEl = container.querySelector('#seconds');

    if (!daysEl || !hoursEl || !minutesEl || !secondsEl) {
        console.warn('[Countdown] Missing timer elements. Retrying...');
        return setTimeout(initCountdown, 100);
    }

    const updateCountdown = () => {
        const now = new Date(new Date().getTime() - timeOffset);
        const distance = startTime - now;

        if (distance <= 0) {
            clearInterval(window.currentCountdownInterval);
            window.currentCountdownInterval = null;
            console.log('[Countdown] Countdown finished — navigating.');

            if (window.spaNavigate) {
                window.spaNavigate(voteUrl);
            } else {
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

    // Start the countdown
    window.currentCountdownInterval = setInterval(updateCountdown, 1000);
    updateCountdown();
};

// Run on first load
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    window.initCountdown();
} else {
    document.addEventListener('DOMContentLoaded', window.initCountdown);
}
