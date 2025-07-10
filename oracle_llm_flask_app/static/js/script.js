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

        // Show data and any explanation from LLM
        let resultText = data.data && Object.keys(data.data).length
            ? "<pre>" + JSON.stringify(data.data, null, 2) + "</pre>"
            : "<i>No tabular data returned.</i>";
        let explanation = data.message ? "<p><b>LLM:</b> " + data.message + "</p>" : "";

        responseMsg.innerHTML = explanation + resultText;
        chat.appendChild(responseMsg);
        chat.scrollTop = chat.scrollHeight;
        document.getElementById("question").value = "";
    });
}
