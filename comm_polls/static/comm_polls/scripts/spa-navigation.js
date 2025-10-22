document.addEventListener('DOMContentLoaded', () => {
    const contentContainer = document.getElementById('main-content');

    // Function to re-initialize all scripts on the page
    const reinitializeScripts = () => {
        // Find all scripts that should be re-run
        const scriptsToRun = [
            'theme-switcher.js',
            'spa-navigation.js', // Re-attach its own listeners
            'showcase.js',
            'typing-animation.js',
            'countdown.js',
            'vote-countdown.js',
            'vote-page.js',
            'signup-validation.js',
            'password-visibility.js',
            'create_poll.js'
        ];

        scriptsToRun.forEach(scriptName => {
            const scriptElement = document.querySelector(`script[src*="${scriptName}"]`);
            if (scriptElement) {
                // To re-execute a script, we must create a new script element
                const newScript = document.createElement('script');
                newScript.src = scriptElement.src;
                newScript.defer = true;
                // Remove the old script to prevent duplicates if any
                scriptElement.remove();
                // Add the new script to the head to execute it
                document.head.appendChild(newScript);
            }
        });
    };

    const loadContent = (url, pushState = true) => {
        // If content container doesn't exist, do a full page load
        if (!contentContainer) { window.location.href = url; return; }

        // Start the fade-out animation on the content container
        contentContainer.style.opacity = '0';

        // Wait for the fade-out to be visible before fetching and replacing content
        setTimeout(() => {
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    
                    const newContentContainer = doc.getElementById('main-content'); // Target the same container
                    if (!newContentContainer) {
                        window.location.href = url; // Fallback to full reload
                        return;
                    }

                    const newContent = newContentContainer.innerHTML;
                    const newTitle = doc.querySelector('title').textContent;

                    // Update the page content and title
                    contentContainer.innerHTML = newContent;
                    document.title = newTitle;

                    // Start the fade-in animation
                    contentContainer.style.opacity = '1';

                    if (pushState) {
                        history.pushState({ path: url }, '', url);
                    }
                    reinitializeScripts();
                })
                .catch(error => {
                    console.error('Error loading page:', error);
                    window.location.href = url; // Fallback to full reload on error
                });
        }, 200); // This delay should match the CSS transition duration
    };

    // Expose loadContent to the global scope to be used by other scripts
    window.spaNavigate = loadContent;

    // Use event delegation on the document body to handle all internal links
    document.body.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        // Check if it's a valid internal link and not a link to an external site or a file
        if (link && link.href.startsWith(window.location.origin) && !link.href.includes('/media/')) {
            e.preventDefault();
            loadContent(link.href);
        }
    });

    // Handle browser back/forward buttons
    window.addEventListener('popstate', (e) => {
        if (e.state && e.state.path) {
            loadContent(e.state.path, false);
        }
    });
});