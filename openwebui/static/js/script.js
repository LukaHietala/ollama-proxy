document.addEventListener("DOMContentLoaded", function () {
    const messages = document.getElementById("messages");
    const userInput = document.getElementById("user-input");

    checkStatus();

    userInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function checkStatus() {
        fetch("/api/health")
            .then((response) => response.json())
            .then((data) => {
                if (
                    data.success &&
                    data.data &&
                    data.data.status === "healthy"
                ) {
                    addMessage("🦙 is healthy", "system");
                } else {
                    addMessage("🦙 is unhealthy", "system");
                }
            })
            .catch(() => {
                addMessage("🦙 is unhealthy", "system");
            });
    }

    function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        if (text === "/clear") {
            clearChat();
            userInput.value = "";
            return;
        }

        addMessage(text, "user");
        userInput.value = "";

        fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success && data.data && data.data.message) {
                    addMessage(data.data.message.content, "assistant");
                } else {
                    addMessage("Failed to get response", "system");
                }
            })
            .catch((error) => {
                console.error(error);
                addMessage("Error sending message", "system");
            });
    }

    function clearChat() {
        fetch("/api/chat/clear", { method: "POST" })
            .then((response) => response.json())
            .then((data) => {
                messages.innerHTML = "";
                if (data.success) {
                    addMessage("Chat cleared", "system");
                } else {
                    addMessage("Failed to clear chat", "system");
                }
            })
            .catch(() => {
                addMessage("Error clearing chat", "system");
            });
    }

    function addMessage(content, type) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = content;
        messages.appendChild(messageDiv);
        window.scrollTo(0, document.body.scrollHeight);
    }
});
