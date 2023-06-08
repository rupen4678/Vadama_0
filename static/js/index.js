// access the data from id l1 when clickme id button is clicked and send to websocket?
function connect(){
    const socket = new WebSocket('ws://' + window.location.host + '/');

    socket.onopen = function(e){
        console.log('opened socket');   
    }
    
    socket.onclose = function(e){
        console.log('closed socket');
        console.log('reconnecting...');
        // Add delay before attempting to reconnect
        setTimeout(function() {
            connect();
        }, 1000);
    }

    socket.onmessage = function(e){
        const data = JSON.parse(e.data);
        alert('on messages' + data.message);
        // Handle incoming message data in a more subtle way
        if (data.type == 'info'){
            const s = document.querySelector('#l2');
            document.getElementById('l2').innerHTML = 'wrote' + data['message'];
    }
        
    };
    const ss = document.getElementById("clickme");
    ss.addEventListener('click', function(){
        const sas = document.getElementById('l1');
        const da = sas.value;
        socket.send(JSON.stringify(
        {
            'type': 'info',
            'message': da,
        }));
    });
}


window.onload = function(){
    connect();
}