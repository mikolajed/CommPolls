document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Function to apply the theme
    const applyTheme = (theme) => {
        if (theme === 'dark') {
            html.setAttribute('data-theme', 'dark');
            themeToggleButton.textContent = '☀️';
        } else {
            html.removeAttribute('data-theme');
            themeToggleButton.textContent = '🌙';
        }
    };

    // Check for saved theme in localStorage or use OS preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    applyTheme(currentTheme);

    // Add click event listener
    themeToggleButton.addEventListener('click', () => {
        const newTheme = html.hasAttribute('data-theme') ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    });
});