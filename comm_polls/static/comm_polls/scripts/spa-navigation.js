document.addEventListener('DOMContentLoaded', () => {
    const contentContainer = document.getElementById('main-content');

    // Load all <script> tags from a fetched HTML document
    const handleScripts = (doc) => {
        // Remove previously managed scripts
        document.querySelectorAll('script[data-spa-managed]').forEach(s => s.remove());

        // Load external scripts
        const newScripts = doc.querySelectorAll('script[src]');
        newScripts.forEach(script => {
            if (!script.src.includes('spa-navigation.js')) {
                const newScript = document.createElement('script');
                newScript.src = script.src;
                newScript.defer = true;
                newScript.setAttribute('data-spa-managed', 'true');
                document.body.appendChild(newScript);
            }
        });

        // Run inline scripts too (for reinitialization)
        const inlineScripts = doc.querySelectorAll('script:not([src])');
        inlineScripts.forEach(script => {
            const newScript = document.createElement('script');
            newScript.textContent = script.textContent;
            newScript.setAttribute('data-spa-managed', 'true');
            document.body.appendChild(newScript);
        });

        // Explicitly re-run any global reinitializers (like countdown)
        if (typeof window.initCountdown === 'function') {
            console.log('[SPA] Reinitializing countdown script.');
            window.initCountdown();
        }
    };

    const loadContent = (url, pushState = true) => {
        if (!contentContainer) { window.location.href = url; return; }

        contentContainer.style.opacity = '0'; // Fade out

        setTimeout(() => {
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContentContainer = doc.getElementById('main-content');

                    if (!newContentContainer) {
                        window.location.href = url;
                        return;
                    }

                    const isAuthenticated = contentContainer.dataset.isAuthenticated === 'true';
                    const loginUrl = contentContainer.dataset.loginUrl;

                    if (!isAuthenticated && newContentContainer.innerHTML.trim() === '' && loginUrl) {
                        window.location.href = loginUrl;
                        return;
                    }

                    contentContainer.innerHTML = newContentContainer.innerHTML;
                    document.title = doc.querySelector('title')?.textContent || document.title;

                    contentContainer.style.opacity = '1'; // Fade in

                    if (pushState) {
                        history.pushState({ path: url }, '', url);
                    }

                    handleScripts(doc);
                })
                .catch(error => {
                    console.error('[SPA] Error loading page:', error);
                    window.location.href = url;
                });
        }, 200); // Match CSS transition time
    };

    // Make globally callable
    window.spaNavigate = loadContent;

    // Intercept internal links
    document.body.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link && link.href.startsWith(window.location.origin) && !link.href.includes('/media/')) {
            e.preventDefault();
            loadContent(link.href);
        }
    });

    // Handle back/forward navigation
    window.addEventListener('popstate', (e) => {
        if (e.state?.path) {
            loadContent(e.state.path, false);
        }
    });
});
