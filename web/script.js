const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

// 🧩 Send user message to backend
async function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  const res = await fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message})
  });
  
  const data = await res.json();
  addMessage(data.response, "bot");
  speakText(data.response); // 👈 Bot talks back
}

// 💬 Add message to chat box
function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// 🎤 Voice recognition using Web Speech API
function startVoice() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  recognition.start();

  recognition.onresult = async (event) => {
    const message = event.results[0][0].transcript;
    addMessage(message, "user");

    const res = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message})
    });
    const data = await res.json();
    addMessage(data.response, "bot");
    speakText(data.response); // 👈 Speak the reply aloud
  };
}

// 🔊 Text-to-speech using Web Speech API
function speakText(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.pitch = 1;
  utterance.rate = 1;
  utterance.volume = 1;
  window.speechSynthesis.speak(utterance);
}
