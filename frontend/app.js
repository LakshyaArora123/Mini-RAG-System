let chatHistory = [];
let selectedFile = null;
let currentFile = null;

async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://127.0.0.1:8000/upload", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  currentFile = data.source;

  addMessage(
    `📄 ${data.filename} indexed (${data.chunks_added} chunks)`,
    "bot"
  );
}

async function summarizeCurrentDocument() {
  console.log("SUMMARY BUTTON CLICKED");

  if (!currentFile) {
    addMessage("assistant", "No document uploaded.");
    return;
  }
}

async function sendMessage() {
  const input = document.getElementById("queryInput");
  const fileInput = document.getElementById("fileInput");
  const query = input.value.trim();

  if (!query) return;

  if (fileInput.files[0]) {
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    selectedFile = data.filename;
    addFileToPanel(data.filename);
    fileInput.value = "";
  }

  addMessage(query, "user");
  input.value = "";

  const res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      query: query,
      source: selectedFile
    })
  });

  const data = await res.json();
  addMessage(data.final_answer, "bot");
}

function addFileToPanel(name) {
  const list = document.getElementById("fileList");
  const div = document.createElement("div");
  div.className = "file-item active";
  div.textContent = name;
  list.appendChild(div);
}

async function clearDocs() {
  await fetch("http://127.0.0.1:8000/clear", { method: "DELETE" });
  document.getElementById("fileList").innerHTML = "";
  selectedFile = null;
  addMessage("All documents cleared.", "bot");
}


function addMessage(text, type) {
  const chatWindow = document.getElementById("chatWindow");
  const msg = document.createElement("div");
  msg.className = `message ${type}`;
  msg.textContent = text;
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
