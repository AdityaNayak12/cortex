const API_BASE = "http://127.0.0.1:8000/api";

const output = document.getElementById("output");
const currentSite = document.getElementById("current-site");
const userIdInput = document.getElementById("user-id-input");
const saveBtn = document.getElementById("btn-save-id");
const statusMsg = document.getElementById("id-status");

// Load saved user ID on popup open
chrome.storage.local.get("userId", ({ userId }) => {
    if (userId) {
        userIdInput.value = userId;
        statusMsg.textContent = "✓ Saved";
        statusMsg.className = "id-status success";
    }
});

// Save user ID to chrome.storage.local
saveBtn.addEventListener("click", () => {
    const id = userIdInput.value.trim();
    if (!id) {
        statusMsg.textContent = "Enter a valid ID";
        statusMsg.className = "id-status error";
        return;
    }
    chrome.storage.local.set({ userId: parseInt(id, 10) }, () => {
        statusMsg.textContent = "✓ Saved";
        statusMsg.className = "id-status success";
    });
});

// Show current tab domain in status bar
chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
    if (tab?.url) {
        try {
            currentSite.textContent = new URL(tab.url).hostname;
        } catch {
            currentSite.textContent = "unknown";
        }
    }
});

async function getStoredUserId() {
    return new Promise((resolve) => {
        chrome.storage.local.get("userId", ({ userId }) => resolve(userId));
    });
}

document.getElementById("btn-analyze").addEventListener("click", async () => {
    const userId = await getStoredUserId();
    if (!userId) {
        output.textContent = "⚠ Please set your User ID above first.";
        return;
    }
    output.textContent = "Loading insights…";
    try {
        const res = await fetch(`${API_BASE}/analyze/${userId}`);
        const data = await res.json();
        output.textContent = data.insights;
    } catch (err) {
        output.textContent = `Error: ${err.message}`;
    }
});

document.getElementById("btn-plan").addEventListener("click", async () => {
    const userId = await getStoredUserId();
    if (!userId) {
        output.textContent = "⚠ Please set your User ID above first.";
        return;
    }
    output.textContent = "Generating plan…";
    try {
        const res = await fetch(`${API_BASE}/plan/${userId}`);
        const data = await res.json();
        output.textContent = data.plan;
    } catch (err) {
        output.textContent = `Error: ${err.message}`;
    }
});
