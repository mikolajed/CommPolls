document.addEventListener('DOMContentLoaded', () => {
    const showcaseChoices = document.querySelectorAll('.showcase-choice');
    if (showcaseChoices.length === 0) return;

    showcaseChoices.forEach(choice => {
        choice.addEventListener('click', () => {
            // Remove 'selected' from all choices in the same poll
            const parentPoll = choice.closest('.showcase-poll');
            parentPoll.querySelectorAll('.showcase-choice').forEach(c => c.classList.remove('selected'));
            // Add 'selected' to the clicked choice
            choice.classList.add('selected');
        });
    });
});