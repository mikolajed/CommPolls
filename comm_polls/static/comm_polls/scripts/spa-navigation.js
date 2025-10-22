// SPA Loader with Countdown Integration
document.addEventListener('DOMContentLoaded', () => {
    const contentContainer = document.getElementById('main-content');
    if (!contentContainer) return;

    // -----------------------------
    // Countdown Initialization
    // -----------------------------
    const initCountdown = () => {
        const countdownContainers = document.querySelectorAll('.vote-countdown');
        countdownContainers.forEach(container => {
            const endTimeStr = container.dataset.endTime;
            const serverTimeStr = container.dataset.serverTime;
            const timerDisplay = container.querySelector('#vote-timer-display');
            const voteButton = container.querySelector('form button[type="submit"]');

            if (!endTimeStr || !serverTimeStr || !timerDisplay) return;

            const endTime = new Date(endTimeStr);
            const serverLoadTime = new Date(serverTimeStr);
            const clientLoadTime = new Date();
            const timeOffset = clientLoadTime.getTime() - serverLoadTime.getTime();

            const updateCountdown = () => {
                const now = Date.now() - timeOffset;
                const distance = endTime.getTime() - now;

                if (distance <= 0) {
                    clearInterval(intervalId);
                    timerDisplay.textContent = 'Poll has ended.';
                    if (voteButton) container.style.display = 'none';
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

            const intervalId = setInterval(updateCountdown, 1000);
            updateCountdown();
        });
    };

    // Expose globally so SPA loader can call
    window.initCountdown = initCountdown;

    // -----------------------------
    // SPA Loader
    // -----------------------------
    const loadExternalScripts = async (scripts) => {
        for (const script of scripts) {
            if (!script.src.includes('spa-navigation.js')) {
                await new Promise((resolve, reject) => {
                    const newScript = document.createElement('script');
                    newScript.src = script.src;
                    newScript.defer = true;
                    newScript.setAttribute('data-spa-managed', 'true');
                    newScript.onload = resolve;
                    newScript.onerror = reject;
                    document.body.appendChild(newScript);
                });
            }
        }
    };

    const runInlineScripts = (scripts) => {
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            newScript.textContent = script.textContent;
            newScript.setAttribute('data-spa-managed', 'true');
            document.body.appendChild(newScript);
        });
    };

    const handleScripts = async (doc) => {
        document.querySelectorAll('script[data-spa-managed]').forEach(s => s.remove());

        const externalScripts = Array.from(doc.querySelectorAll('script[src]'));
        const inlineScripts = Array.from(doc.querySelectorAll('script:not([src])'));

        await loadExternalScripts(externalScripts);
        runInlineScripts(inlineScripts);

        if (typeof window.initCountdown === 'function') {
            console.log('[SPA] Reinitializing countdown.');
            window.initCountdown();
        }
    };

    const loadContent = (url, pushState = true) => {
        if (!contentContainer) {
            window.location.href = url;
            return;
        }

        const onTransitionEnd = () => {
            contentContainer.removeEventListener('transitionend', onTransitionEnd);

            fetch(url)
                .then(response => response.text())
                .then(async html => {
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
                    document.title = doc.querySelector('title')?.textContent?.trim() || document.title;

                    if (pushState) history.pushState({ path: url }, '', url);

                    await handleScripts(doc);

                    contentContainer.style.opacity = '1'; // fade in
                })
                .catch(error => {
                    console.error('[SPA] Error loading page:', error);
                    window.location.href = url;
                });
        };

        contentContainer.addEventListener('transitionend', onTransitionEnd);
        contentContainer.style.opacity = '0'; // fade out
    };

    // Expose SPA navigation
    window.spaNavigate = loadContent;

    // Intercept internal links
    document.body.addEventListener('click', e => {
        const link = e.target.closest('a');
        if (
            link &&
            link.href.startsWith(window.location.origin) &&
            !link.href.includes('/media/') &&
            link.target !== '_blank'
        ) {
            e.preventDefault();
            loadContent(link.href);
        }
    });

    // Handle back/forward navigation
    window.addEventListener('popstate', e => {
        if (e.state?.path) loadContent(e.state.path, false);
    });

    // Initialize countdowns on first load
    initCountdown();
});
