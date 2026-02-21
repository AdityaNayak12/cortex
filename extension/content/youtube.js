// YouTube content script — tracks video watch sessions
(() => {
    let subject = "YouTube";
    let startTime = null;
    let videoTitle = null;

    function getTitle() {
        return document.querySelector("h1.ytd-video-primary-info-renderer")?.innerText || document.title;
    }

    function startTracking() {
        startTime = Date.now();
        videoTitle = getTitle();
        console.log(`[Cortex] Started tracking: ${videoTitle}`);
    }

    function stopTracking() {
        if (!startTime) return;
        const durationMinutes = (Date.now() - startTime) / 60000;
        startTime = null;

        chrome.runtime.sendMessage({
            type: "TRACK_ACTIVITY",
            payload: {
                user_id: 1, // TODO: replace with real user ID from storage
                subject,
                topic: videoTitle,
                duration_minutes: parseFloat(durationMinutes.toFixed(2)),
            },
        });
    }

    document.addEventListener("visibilitychange", () => {
        if (document.hidden) stopTracking();
        else startTracking();
    });

    window.addEventListener("beforeunload", stopTracking);

    startTracking();
})();
