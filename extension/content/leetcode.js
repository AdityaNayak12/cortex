// LeetCode content script — tracks problem-solving sessions
(() => {
    let subject = "LeetCode";
    let startTime = null;
    let problem = null;

    function getProblemTitle() {
        return document.querySelector('[data-cy="question-title"]')?.innerText
            || document.title.replace(" - LeetCode", "").trim();
    }

    function startTracking() {
        startTime = Date.now();
        problem = getProblemTitle();
        console.log(`[Cortex] Started tracking LeetCode: ${problem}`);
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
                topic: problem,
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
