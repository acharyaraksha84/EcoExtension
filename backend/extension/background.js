// background.js
const API_URL = "http://localhost:8000/analyze"; // FastAPI backend

chrome.action.onClicked.addListener((tab) => {
  chrome.sidePanel.open({ windowId: tab.windowId });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyzeProduct") {
    if (request.text) {
      analyzeText(request.text, sendResponse);
      return true;
    }
  }
});

function analyzeText(text, sendResponse) {
  fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  })
    .then(res => res.json())
    .then(data => {
      if (data.alternatives && Array.isArray(data.alternatives)) {
        data.alternatives = data.alternatives.map((alt) => ({
          ...alt,
          image: alt.image?.startsWith("http") ? alt.image : "https://placehold.co/76x76"
        }));
      }

      sendResponse({ status: "success", data });
      // broadcast to panel
      chrome.runtime.sendMessage({ action: "updateAnalysis", data });
    })
    .catch(err => {
      sendResponse({ status: "error", error: err.message });
    });
}

// 🔄 detect when product page reloads
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && /^https?:/.test(tab.url)) {
    chrome.tabs.sendMessage(tabId, { action: "triggerAnalysis" });
  }
});
