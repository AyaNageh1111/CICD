function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function sendMessage() {
  // Get the message from the input field
  const message = document.getElementById('chat-message').value;

  // Clear the input field
  document.getElementById('chat-message').value = '';

  // Create a new chat message element
  const messageElement = document.createElement('div');
  messageElement.classList.add('chat-message');
  messageElement.innerHTML = message;

  // Append the chat message element to the chat container
  const chatContainer = document.getElementById('chat-container');
  chatContainer.appendChild(messageElement);
}