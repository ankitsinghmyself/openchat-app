document.addEventListener('DOMContentLoaded', () => {
  var socket = io();
  //setting of default room
  let room = "Lounge";
  joinRoom("Lounge");

  //dispaly incomming msg
  socket.on('message', data => {
    const p = document.createElement('p');
    const span_username = document.createElement('span');
    const span_timestamp = document.createElement('span');
    const br = document.createElement('br');
    // Display user's own message
    if (data.username == username) {
      p.setAttribute("class", "my-msg");

      // Username
      span_username.setAttribute("class", "my-username");
      span_username.innerText = data.username;

      // Timestamp
      span_timestamp.setAttribute("class", "timestamp");
      span_timestamp.innerText = data.time_stamp;

      // HTML to append
      p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

      //Append
      document.querySelector('#display-message-section').append(p);
    }
    // Display other users' messages
    else if (typeof data.username !== 'undefined') {
      p.setAttribute("class", "others-msg");

      // Username
      span_username.setAttribute("class", "other-username");
      span_username.innerText = data.username;

      // Timestamp
      span_timestamp.setAttribute("class", "timestamp");
      span_timestamp.innerText = data.time_stamp;

      // HTML to append
      p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

      //Append
      document.querySelector('#display-message-section').append(p);
    }

    if (data.username) {
      span_username.innerHTML = data.username;
      span_timestamp.innerHTML = data.time_stamp;


      p.innerHTML = span_username.outerHTML + br.outerHTML
        + data.msg + br.outerHTML + span_timestamp.outerHTML;

      document.querySelector('#display-message-section').append(p);

    }
    else {
      printSysMsg(data.msg);
    }
    scrollDownChatWindow();
  });

  //send msg
  document.querySelector('#send_message').onclick = () => {
    socket.send({
      'msg': document.querySelector('#user_message').value
      , 'username': username, 'room': room
    });
    //clear input area
    document.querySelector('#user_message').value = '';
  }

  //room selection
  document.querySelectorAll('.select-room').forEach(p => {
    p.onclick = () => {
      let newRoom = p.innerHTML;
      if (newRoom == room) {
        msg = `You are in ${room} room.`
        printSysMsg(msg);

      }
      else {
        leaveRoom(room);
        joinRoom(newRoom);
        room = newRoom;
      }

    }
  });

  //leave room
  function leaveRoom(room) {
    socket.emit('leave', { 'username': username, 'room': room });
  }

  //join room

  function joinRoom(room) {
    socket.emit('join', { 'username': username, 'room': room });
    // Highlight selected room
    document.querySelector('#' + CSS.escape(room)).style.color = "#ffc107";
    document.querySelector('#' + CSS.escape(room)).style.backgroundColor = "white";
    //clear msg
    document.querySelector('#display-message-section').innerHTML = ''
    //autofocus on textbox
    document.querySelector('#user_message').focus();

  }

  //Print System msg
  function printSysMsg(msg) {
    const p = document.createElement('p');
    p.innerHTML = msg;
    document.querySelector('#display-message-section').append(p);
  }
  
  // Scroll chat window down
  function scrollDownChatWindow() {
    const chatWindow = document.querySelector("#display-message-section");
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
});