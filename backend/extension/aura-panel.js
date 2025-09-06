// aura-panel.js
document.addEventListener("DOMContentLoaded", () => {
  function updateScore(score) {
    const scoreDiv = document.querySelector(".score");
    const scoreValue = document.querySelector(".score .value");
    if (scoreDiv && scoreValue) {
      scoreDiv.style.setProperty("--percent", score);
      scoreValue.innerHTML = `${score}<span style="font-size:12px;color:var(--muted);font-weight:600">/100</span>`;
    }
  }

  function updateAlternatives(alternatives) {
    const altGrid = document.querySelector(".alt-grid");
    if (!altGrid) return;
    altGrid.innerHTML = "";
    alternatives.forEach((alt) => {
      const card = document.createElement("div");
      card.className = "product-card";
      card.innerHTML = `
        <img src="${alt.image || "https://placehold.co/76x76"}" alt="${alt.name}" />
        <div class="pname">${alt.name}</div>
      `;
      altGrid.appendChild(card);
    });
  }

  // 🔄 listen for background broadcasts
  chrome.runtime.onMessage.addListener((request) => {
    if (request.action === "updateAnalysis" && request.data) {
      updateScore(request.data.score);
      updateAlternatives(request.data.alternatives);
    }
  });
});
