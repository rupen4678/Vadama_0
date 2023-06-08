function connect () {
  const pathname = window.location.pathname;
  const productId = pathname.split("/")[2];
  
  console.log('product_id: ' + productId + ' user_id: ' );
  let socket = new WebSocket('ws://' + window.location.host + '/'+ 'product' + '/' + productId + '/');

  socket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  updateUI(data);
};
  
  socket.onclose = function(e){
    console.log('closed socket with error' + e.message);
    console.log('reconnecting...');

    //Add delay before attempting to reconnect
    setTimeout(function() {
        socket = connect();
    }, 1000);
  };

  // try {
  //   const ale = document.getElementById('emptyalert');
  //   const ms = document.getElementById('commentss');
  //   const se = document.getElementById('corn');
  //   se.addEventListener('submit', function(e){
  //     e.preventDefault();
      
  //       if ( ms.value !== ''){
  //         ale.style.display = 'hidden';
  //         const msg = ms.value;
  //         console.log('i sent the data from here as'+ msg);
  //         socket.send(JSON.stringify({
  //           'type' : 'comm',
  //           'product_id': productId,
  //           'message' : msg,
  //         }));
  //         ms.value = '';
  //       }else {
  //         ale.style.display = 'block';
  //       }
      
  //   })
  // } catch (error) {
  //   console.error('the error is ' + error);
  // }
  
  const se = document.getElementById('send');
  const ms = document.getElementById('commentss');
  se.addEventListener('click', function(event) {
    event.preventDefault();
    const msg = ms.value;
    console.log('i sent the data from here as'+ msg);
    socket.send(JSON.stringify({
      'type' : 'comm',
      'product_id': productId,
      'message' : msg,
    }));
    ms.value = '';
  });

function updateUI(data) {
  // console.log(data);
  if (data.type == 'comm') {
    // Clear the existing comments
    console.log('inside ');
    document.getElementById('datash').innerHTML = '';

    // Get the comments data
    const its = data.message;
    // Loop through the comments and create the HTML for each comment
    const items = JSON.parse(its);
    for (const item of items) {
      const { fields } = item;
      if (fields) {
        const { comment, comment_date, man } = fields || {};
      console.log('showing Comment: ${comment}');
      // Create the HTML for the comment
      const html = `
        <div class='panel'>
          <div class="panel-body">
            <div class="media-block">
              <a class="media-left" href="#"><img class="img-circle img-sm" alt="Profile Picture" src="https://bootdey.com/img/Content/avatar/avatar1.png"></a>
              <div class="media-body">
                <div class="mar-btm">
                  <a id="msg1" class="btn-link text-semibold media-heading box-inline">${man}</a>
                  <script>
                    const receiver = document.getElementById('msg1').text;
                    alert(msg1.text);
                    receiver.addEventListener('click', function{
                      var sender = '{{ request.user.username }}';
                      var url = '/chat/users/' + receiver + '_' + sender;
                      console.log('redirecting to' + url);
                      windows.location.href = url;
                    })
                  </script>
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
};} 
document.addEventListener("DOMContentLoaded", function() {
  connect();
});