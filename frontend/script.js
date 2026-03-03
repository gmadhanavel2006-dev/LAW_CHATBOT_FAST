const BACKEND_URL = "https://YOUR_RENDER_URL.onrender.com";

function addBubble(text, sender) {
  const chat = document.getElementById("chat");
  const bubble = document.createElement("div");
  bubble.className = `bubble ${sender}`;
  bubble.innerText = text;
  chat.appendChild(bubble);
  chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
  const textarea = document.getElementById("message");
  const message = textarea.value.trim();

  if (!message) return;

  addBubble(message, "user");
  textarea.value = "";

  addBubble("Thinking...", "bot");

  try {
    const res = await fetch(`${BACKEND_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message,
        country: "india",
        role: "citizen"
      })
    });

    const data = await res.json();

    // Remove "Thinking..."
    const chat = document.getElementById("chat");
    chat.removeChild(chat.lastChild);

    addBubble(data.response, "bot");

  } catch {
    addBubble("Backend not reachable. Please try again.", "bot");
  }
}