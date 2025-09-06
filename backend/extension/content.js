// content.js
(function () {
  // scrape Amazon product text
  function getProductText() {
    let title = document.querySelector("#productTitle")?.innerText || "";
    let bullets = [...document.querySelectorAll("#feature-bullets li")]
      .map((el) => el.innerText.trim())
      .join(" ");
    return `${title} ${bullets}`.trim();
  }

  // respond to background
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getProductText") {
      sendResponse({ text: getProductText() });
    }
    if (request.action === "triggerAnalysis") {
      chrome.runtime.sendMessage({
        action: "analyzeProduct",
        text: getProductText(),
        url: window.location.href
      });
    }
  });
})();
