const BACKEND_URL = "https://global-ai-legal-assistant.onrender.com";

async function getLegalGuidance() {
  const message = document.getElementById("message").value.trim();
  const country = document.getElementById("country").value;
  const role = document.getElementById("role").value;
  const output = document.getElementById("output");

  if (!message) {
    output.innerHTML = "<b>Please enter a legal issue.</b>";
    return;
  }

  output.innerHTML = "⏳ Waking up server… please wait (first request may take 30s)";

  const controller = new AbortController();
  setTimeout(() => controller.abort(), 45000); // 45s timeout

  try {
    const res = await fetch(`${BACKEND_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      body: JSON.stringify({
        message: message,
        country: country,
        role: role
      })
    });

    const data = await res.json();
    output.innerHTML = `<pre>${data.response}</pre>`;
  } catch (err) {
    output.innerHTML =
      "⚠️ Server is waking up or temporarily unavailable. Please try again in 30 seconds.";
  }
}