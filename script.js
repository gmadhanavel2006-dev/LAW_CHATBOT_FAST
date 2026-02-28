const API_URL = "https://law-chatbot-fast.onrender.com/chat";

async function getLegalGuidance() {
  const issue = document.getElementById("issue").value.trim();
  const country = document.getElementById("country").value;
  const role = document.getElementById("role").value;
  const resultBox = document.getElementById("result");

  if (!issue) {
    resultBox.innerHTML = "❌ Please describe your legal issue.";
    return;
  }

  resultBox.innerHTML = "⏳ Connecting to legal server...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_input: issue,
        country: country,
        user_role: role
      })
    });

    const data = await response.json();

    let html = "<h3>⚖️ Legal Guidance</h3><ul>";
    for (const key in data) {
      html += `<li><b>${key.replace(/_/g, " ")}:</b> ${data[key]}</li>`;
    }
    html += "</ul>";

    resultBox.innerHTML = html;

  } catch (err) {
    console.error(err);
    resultBox.innerHTML = "❌ Unable to connect to the legal server.";
  }
}