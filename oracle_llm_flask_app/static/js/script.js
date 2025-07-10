
function sendQuestion() {
    const question = document.getElementById("question").value;
    fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question})
    })
    .then(res => res.json())
    .then(data => {
        const chat = document.getElementById("chat-box");
        const userMsg = document.createElement("div");
        userMsg.innerHTML = "<b>You:</b> " + question;
        chat.appendChild(userMsg);

        const responseMsg = document.createElement("div");
        responseMsg.innerHTML = "<b>Gemini:</b><pre>" + JSON.stringify(data.data, null, 2) + "</pre>";
        chat.appendChild(responseMsg);

        chat.scrollTop = chat.scrollHeight;
        document.getElementById("question").value = "";
    });
}
