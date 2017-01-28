var app = require('express')();
var server = require('http').Server(app);
var io = require('socket.io')(server);

var color = "red";

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function (socket) {
  socket.emit('color_update', { color: 'red' });

  setInterval(function(){
		socket.emit('color_update', { color: color });
		if(color == "red")
			color = "blue"
		else
			color = "red"
	}, 100);
});

server.listen(3000, function() {
	console.log("server running on port 3000")
});


