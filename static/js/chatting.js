console.log('dry check chatting.js');

function goBack() {
  window.history.back();
}

function connect() {
  const pathname = window.location.pathname;
  const chat = pathname.split("/")[3];

  console.log('connecting');
  var socket = new WebSocket('ws://' + window.location.host + '/users/chat/' + chat + '/');
  
  //i am applying clever solution here when connected 
  socket.onopen = function (e) {
    console.log('opened socket for chatting and requesting data ');
    // Request previous chat data from the server
    socket.send(JSON.stringify({
      'type': 'get_initial_data',
    })); 
  }

  socket.onclose = function (e) {
    console.log('reconnecting chatting...');
    // Add delay before attempting to reconnect
    setTimeout(function () {
      connect();
    }, 5000);
  }

  socket.onmessage = function (e) {
    const da = JSON.parse(e.data);
    if (da.type == "initial_data"){
      fillUI(e);

    }else if (da.type == "pvt_msg"){
      updateUI(e);

    }else if(da.type == "users_list"){
      updateUsers(e);
    }
    else{
      console.log('got unknown data from server');
    }
  }

  //is sending the message to server 
  var btnClicked = document.getElementById('sendz');
  var message = document.getElementById('messagez');

  btnClicked.addEventListener('click', function (event) {
    event.preventDefault();
    console.log('pvtmsg sent' + message.value);
    const someName = document.querySelector('.chat_list.active_chat');
    let receiver1;
    if (someName){
      const final_name = someName.querySelector('.chat_ib h5');
      receiver1 = final_name.firstChild.textContent.trim();
      console.log('username' + receiver1);
    }
    socket.send(JSON.stringify({
      'type': 'pvt_msg',
      'message': message.value,
      'receiver' : receiver1,
    }));
    message.value = '';
  });

  //this will handle the user list click 

  var h5Elements = document.querySelectorAll('.chat_ib h5');
  h5Elements.forEach(function(h5Element, index) {
    h5Element.addEventListener('click', function() {
      var username = this.firstChild.textContent.trim();
      console.log(username);
      $.ajax({
        type: 'GET',
        url : 'users/chat/data',
        data : {
          'data' : username,
        },
        dataType: 'json',
        success: function(response){
          const r = JSON.stringify(response.data)
          console.log('success data received' + r);
          // just shortcut to get the receiver user for 
          // updating the chat

          socket.send(JSON.stringify({
            'type': 'initial_data',
            'receiver': r,
          }));
        },
        error: function(response){
          console.log('got error' + response);
        }
      })
    });
  });
  function fillUI(e) {
    var cuser = document.getElementById('username').textContent;
    var da = JSON.parse(e.data);
    const messages = da.message;
    const authors = da.author;

    var s = document.getElementsByClassName('msg_history')[0];
    s.innerHTML = '';
    for (var i = 0; i < messages.length; i++) {
      var message = messages[i];
      var author = authors[i];

      if (cuser == author) {
        var newMsg = sentMessage(author, message);
        s.innerHTML += newMsg;
      } else {
        var newMsg = receivedMessage(author, message);
        s.innerHTML += newMsg;
      }
    }
  }

  function updateUI(e) {
    console.log('inside updateUI');
    var cuser = document.getElementById('username').textContent;
    var da = JSON.parse(e.data);
    console.log('comparing with' + da.author);
    console.log('this fucker' + cuser);
    var s = document.getElementsByClassName('msg_history')[0];
    if (da.type == 'pvt_msg') {
      if (da.author == cuser){
        var j = sentMessage(da.author, da.message);
        s.innerHTML += j;
      }
      else{
        var newMsg = receivedMessage(da.sender, da.message);
        s.innerHTML += newMsg;
      }
    } else {
      console.log('holy cow undefined or garbage ignoring !!!1' + da.msg);
    }
  }

  function updateUsers(e){
    const da = JSON.parse(e.data)
    if (da.type = "users_list"){
      const chatbox = getElementsByClassName('inbox_chat');
      const users = da.users;
      for (var i = 0; i < users.length; i++) {
        user = users[i];
        html = addUsers(user);
        chatbox.innerHTML += html;
      }
    }
  }

  function addUsers(r){

      html = ` <div class="inbox_chat">
      <div class="chat_list active_chat">
        <div class="chat_people">
          <div class="chat_img"> <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="sunil"> </div>
          <div class="chat_ib">
            <h5>${r}<span class="chat_date">Dec 25</span></h5>
            <p>Test, which is a new approach to have all solutions 
              astrology under one roof.</p>
          </div>
          </div>
        </div>
      </div>`;
      return html;
  }

  function receivedMessage(author, message) {
    const ti = getCurrentTime();
    const html = `<div class="incoming_msg">
    <div class="incoming_msg_img"> <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="sunil"> </div>
    <div class="received_msg">
      <div class="received_withd_msg">
        <p>${message}</p>
        <span class="time_date float-left"> ${ti}   |    Today</span><span>${author}</span></div>
      </div>
    </div>`;
    return html;
  }
  function sentMessage(author, message){
    var o = getCurrentTime();
    html = `
    <div class="outgoing_msg">
      <div class="sent_msg">
        <p>${message}</p>
        <span class="time_date"> ${o}  |    Today</span><span>${author}</span>
      </div>
    </div>`;
    return html;
  };

  function getCurrentTime() {
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
  }
}
window.onload = function () {
  connect();

};
