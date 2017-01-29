var app = require('express')();
var server = require('http').Server(app);
var io = require('socket.io')(server);

var spawn = require("child_process").spawn;



app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});


io.on('connection', function (socket) {

		var data_string
		console.log("connected")
		var process = spawn('python',["audio.py"]);
		process.stdout.on('data', function (data){
			console.log("data")
			console.log(data.toString())
			data_string = data.toString()
		});

		var interval = setInterval(function(str1, str2) {
		  socket.emit('color_update', { color: data_string});
		}, 100);

});

server.listen(5000, function() {
	console.log("server running on port 5000")
});


