// YouTube content script — tracks video watch sessions
(() => {
    let subject = "YouTube";
    let startTime = null;
    let videoTitle = null;

    let currentUrl = location.href;

    function getTitle() {
        // Try the modern video title element first, fallback to document title
        const titleEl = document.querySelector('h1.ytd-watch-metadata yt-formatted-string') ||
            document.querySelector('h1.title yt-formatted-string');
        return titleEl ? titleEl.innerText : document.title.replace(/^\(\d+\)\s/, ''); // Remove notification count like "(3) "
    }

    function startTracking() {
        if (!location.pathname.startsWith('/watch')) return; // Only track watch pages

        startTime = Date.now();
        // Delay getting title slightly to let YouTube SPA render the new title
        setTimeout(() => {
            videoTitle = getTitle();
            console.log(`[Cortex] Started tracking YouTube video: ${videoTitle}`);
        }, 1500);
    }

    function stopTracking() {
        if (!startTime) return;
        const durationMinutes = (Date.now() - startTime) / 60000;
        const trackedTitle = videoTitle || getTitle()
        startTime = null;

        console.log(`[Cortex] Stopped tracking YouTube: ${trackedTitle} (${durationMinutes.toFixed(2)} min)`);

        chrome.storage.local.get("userId", ({ userId }) => {
            if (!userId) {
                console.warn("[Cortex] No user ID set — skipping tracking. Set it in the popup.");
                return;
            }
            chrome.runtime.sendMessage({
                type: "TRACK_ACTIVITY",
                payload: {
                    user_id: userId,
                    subject,
                    topic: trackedTitle,
                    duration_minutes: parseFloat(durationMinutes.toFixed(2)),
                },
            });
        });
    }

    // 1. Handle tab visibility changes (switching tabs)
    document.addEventListener("visibilitychange", () => {
        if (document.hidden) stopTracking();
        else startTracking();
    });

    // 2. Handle tab closing/refreshing
    window.addEventListener("beforeunload", stopTracking);

    // 3. Handle YouTube's SPA navigation (clicking a video from the sidebar)
    setInterval(() => {
        if (location.href !== currentUrl) {
            currentUrl = location.href;
            stopTracking();
            startTracking();
        }
    }, 1000);

    // Initial start
    startTracking();
})();
