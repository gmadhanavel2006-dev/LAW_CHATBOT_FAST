async function getLegalGuidance() {
  const issue = document.getElementById("issue").value;
  const country = document.getElementById("country").value;
  const role = document.getElementById("role").value;
  const resultBox = document.getElementById("result");

  resultBox.innerHTML = "<p>⏳ Analyzing your legal issue...</p>";

  try {
    const response = await fetch(
      "https://law-chatbot-fast.onrender.com/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_input: issue,
          country: country,
          user_role: role,
        }),
      }
    );

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();

    resultBox.innerHTML = `
      <div class="card">
        <h3>⚖ Legal Analysis</h3>
        <p><b>Issue:</b> ${data.issue}</p>
        <p><b>Law Section:</b> ${data.law_section}</p>
        <p><b>Offence:</b> ${data.offence}</p>
        <p><b>Punishment:</b> ${data.punishment}</p>
        <p><b>Explanation:</b> ${data.explanation}</p>
        <h4>📌 Next Steps</h4>
        <ul>
          ${data.next_steps.map(step => `<li>${step}</li>`).join("")}
        </ul>
      </div>
    `;
  } catch (error) {
    resultBox.innerHTML = `
      <p class="error">❌ Unable to connect to the legal server.</p>
    `;
  }
}