const API_URL = "https://YOUR_RENDER_URL/chat";

async function sendQuery() {
    const input = document.getElementById("userInput").value;
    const country = document.getElementById("country").value;
    const role = document.getElementById("role").value;
    const result = document.getElementById("result");

    if (!input.trim()) {
        result.innerText = "⚠️ Please describe your legal issue.";
        return;
    }

    result.innerText = "⏳ Analyzing with Royal Legal Intelligence...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_input: input,
                country: country,
                user_role: role
            })
        });

        const data = await response.json();
        result.innerText = JSON.stringify(data, null, 2);

    } catch {
        result.innerText = "❌ Unable to connect to the legal server.";
    }
}