document.addEventListener('DOMContentLoaded', () => {
    const countdownContainer = document.querySelector('.countdown-container');
    if (!countdownContainer) return;

    const startTime = new Date(countdownContainer.dataset.startTime);
    const voteUrl = countdownContainer.dataset.voteUrl;
    const pollId = countdownContainer.dataset.pollId;

    const daysEl = document.getElementById('days');
    const hoursEl = document.getElementById('hours');
    const minutesEl = document.getElementById('minutes');
    const secondsEl = document.getElementById('seconds');

    const updateCountdown = () => {
        const now = new Date();
        const distance = startTime - now;

        if (distance <= 0) {
            clearInterval(countdownInterval);
            // Use AJAX to fetch the vote form and replace the content
            fetch(voteUrl)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContent = doc.querySelector('.container').innerHTML;
                    document.querySelector('.container').innerHTML = newContent;
                })
                .catch(error => {
                    console.error('Error fetching vote page:', error);
                    // Fallback to a simple redirect if AJAX fails
                    window.location.href = voteUrl;
                });
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