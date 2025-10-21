document.addEventListener('DOMContentLoaded', () => {
    const chartCanvas = document.getElementById('resultsChart');
    if (!chartCanvas) {
        return;
    }

    const ctx = chartCanvas.getContext('2d');
    const labels = JSON.parse(chartCanvas.dataset.labels);
    const votes = JSON.parse(chartCanvas.dataset.votes);

    const data = {
        labels: labels,
        datasets: [{
            label: 'Votes',
            data: votes,
            backgroundColor: 'rgba(52, 152, 219, 0.6)',
            borderColor: 'rgba(52, 152, 219, 1)',
            borderWidth: 1
        }]
    };

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            scales: { y: { beginAtZero: true } }
        }
    });
});