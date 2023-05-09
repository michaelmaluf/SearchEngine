document.addEventListener("DOMContentLoaded", function () {
  const searchForm = document.querySelector("#search-form");
  const resultsContainer = document.querySelector("#results-container");

  searchForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const query = document.querySelector("#search-input").value;

    try {
      const response = await fetch(`/search?query=${query}`);
      const results = await response.json();

      let resultsHtml = "";
      for (let result of results) {
        resultsHtml += `
          <div class="result-box">
            <div class="details">
              <h2>${result.username}</h2>
              <p>${result.content}</p>
            </div>
            <div class="score">${result.score}</div>
          </div>
        `;
      }

      resultsContainer.innerHTML = resultsHtml;
    } catch (error) {
      console.error(error);
      resultsContainer.innerHTML =
        "<p>There was an error processing your request.</p>";
    }
  });
});

