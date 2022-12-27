  console.log('dry check for products.js');

  function connect () {
    const pathname = window.location.pathname;
    const productId = pathname.split("/")[2];
    
    console.log('product_id: ' + productId + ' user_id: ' );
    const socket = new WebSocket('ws://' + window.location.host + '/'+ 'product' + '/' + productId + '/');
   
    socket.onmessage = function(e) {
      try {
        const data = JSON.parse(e.data);
        updateUI(data);
      } catch (e) {
        console.error(e);
        alert("error json data in onmessage");
      }
    }
    
    socket.onclose = function(e){
      console.log('closed socket with error' + e.message);
      console.log('reconnecting...');

      setTimeout(function() {
          socket = connect();
      }, 1000);
      socket.close();
    };
    socket.addEventListener('message', (event) => {
      try {
        const data = JSON.parse(event.data);
        updateUI(data);
      } catch (e) {
        console.error(e);
        alert('error parsing dta in event');
      } 
    });

    document.querySelector('#send').onkeyup = function(e) {
      if (e.keyCode === 13) {
        document.querySelector('#send').click();
      }
  };

  const message = document.querySelector('#commentss').value;
  const ale = document.getElementById('emptyalert');
        
  document.addEventListener('click' ,function(e) {
    if (e.target.id === 'send') {
      e.preventDefault();
      const ms = document.getElementById('commentss');
      if (!ms.value) {
        ale.style.display = 'none';
        return false
      } else {
        ale.style.display = "block";                        
      }
      const message = ms.value;
      socket.send(JSON.stringify({
        'type': 'comm',
        'product_id' : productId,
        'message': message,
    }));
    ms.value = '';
    }
  });

  function updateUI(data) {
    if (data.type == 'comm') {
      console.log('inside ');
      document.getElementById('datash').innerHTML = '';
  
      const its = data.message;
      // console.log(its);
      const comments = JSON.parse(its);
      for (const item of comments) {
        // console.log(item);
        const { fields } = item;
        if (item.fields){
          const { comment, comment_date, username } = item || {};
        const html = `
          <div class='panel'>
            <div class="panel-body">
              <div class="media-block">
                <a class="media-left" href="#"><img class="img-circle img-sm" alt="Profile Picture" src="https://bootdey.com/img/Content/avatar/avatar1.png"></a>
                <div class="media-body">
                  <div class="mar-btm">
                    <a href="#" class="btn-link text-semibold media-heading box-inline">${username}</a>
                    <p cass="text-muted text-sm"><i class="fa fa-mobile fa-lg"></i>commented on:-${comment_date}</p>
                  </div>
                  <p>${comment}</p>
                  <div class="pad-ver">
                    <div class="btn-group">
                      <a class="btn btn-sm btn-default btn-hover-success" href="#">like<i class="fa fa-thumbs-up"></i></a>
                      <a class="btn btn-sm btn-default btn-hover-danger" href="#">comment<i class="fa fa-search"></i></a>
                    </div>
                  </div>
                  <hr>
              </div>
            </div>
          </div>
        `;
  
        // Append the HTML to the datash element
        document.getElementById('datash').innerHTML += html;
      }
    }}
  };  
}
connect();
