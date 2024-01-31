// chat/static/room.js

console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById("roomName").textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
  if (document.querySelector("option[value='" + value + "']")) return;
  let newOption = document.createElement("option");
  newOption.value = value;
  newOption.innerHTML = value;
  onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
  let oldOption = document.querySelector("option[value='" + value + "']");
  if (oldOption !== null) oldOption.remove();
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter key
    chatMessageSend.click();
  }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function () {
  if (chatMessageInput.value.length === 0) return;

  //Mesage
  let message = { message: chatMessageInput.value}
  if(onlineUsersSelector.selectedOptions.length === 1)
    message['to'] = onlineUsersSelector.options[onlineUsersSelector.selectedIndex].value;

  // forward the message to the WebSocket
  chatSocket.send(
    JSON.stringify(message)
  );
  chatMessageInput.value = "";
};

// WebSocket WebSocket WebSocket

let chatSocket = null;

function connect() {
  const proto = window.location.protocol.indexOf('https') !== -1? 'wss': 'ws';
  const url = `${proto}://${window.location.host}/ws/chat/${roomName}/`;

  chatSocket = new WebSocket( url );

  chatSocket.onopen = function (e) {
    console.log("Successfully connected to the WebSocket.");
  };

  chatSocket.onclose = function (e) {
    console.log(
      "WebSocket connection closed unexpectedly. Trying to reconnect in 2s..."
    );
    setTimeout(function () {
      console.log("Reconnecting...");
      connect();
    }, 2000);
  };

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);

    switch (data.type) {
      case "chat_message":
        chatLog.value += `${data.room !== roomName ? `${data.room}/` : ''}${data.user}: ${data.message}\n`;
        break;
      case "private_message":
        chatLog.value += `private msg from ${data.user}: ${data.message}\n`;
        break;
      case "user_list":
        data.users.map(item => {
          onlineUsersSelectorAdd(item)
        })
        break;
      case "user_join":
        onlineUsersSelectorAdd(data.user)
        chatLog.value += `${data.user} joined room ${data.room !== roomName ? data.room : ''}\n`;
        break;
      case "user_leave":
        onlineUsersSelectorRemove(data.user)
        chatLog.value += `${data.user} left room ${data.room !== roomName ? data.room : ''}\n`;
        break;
      default:
        console.error(`Unknown message type: ${data.type}`);
        break;
    }

    // scroll 'chatLog' to the bottom
    chatLog.scrollTop = chatLog.scrollHeight;
  };

  chatSocket.onerror = function (err) {
    console.log("WebSocket encountered an error: " + err.code, err.reason, err.data);
    console.log("Closing the socket.");
    chatSocket.close();
  };
}
connect();
