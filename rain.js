var Connection = require('tedious').Connection;
var Request = require('tedious').Request;
var http = require('http');
var io = require('socket.io');
var server = http.createServer(function (req, res){
    // http create for client accessing
});
//server.listen(52724);               // server has to listen port number 52724 (52723 is for app which is chatting with others)
server.listen(1685);
var sock = io.listen(server);       // 'socket' has parameter named 'socket'. so I changed it to sock

sock.on("connection", function(socket){
    socket.on("List", function(data){
        console.log("List function reached");
        const {spawn} = require("child_process");
        const pyProg = spawn('python', ['./VultrMaker.py', 'listall']);
        pyProg.stdout.on('data', function(pyData){
            console.log("Process end");
            console.log(pyData.toString());
            socket.emit("RespondList", pyData.toString());
        })
    });
    // {"dcid":25, "vpsplanid":201, "osid":216}
    socket.on("CreateRequest", function(data){
        console.log(data);
        var ParsedData = JSON.parse(JSON.stringify(data));
        var dcid = data['dcid'];
        var vpsplanid = data['vpsplanid'];
        var osid = data['osid'];
        const {spawn} = require("child_process");
        const pyProg = spawn('python', ['./VultrMaker.py', 'create', dcid, vpsplanid, osid]);
        pyProg.stdout.on('data', function(pyData) 
        {
            var len = pyData.toString().length;
            var ParsedData = "";
            for(var i=0; i<len; i++) {
                if(!isNaN(parseInt(pyData.toString()[i], 10))){
                    ParsedData = ParsedData + pyData.toString()[i];
                }
            }
            var ParsedInt = parseInt(ParsedData,10);
            console.log("ParssedData : " + ParsedInt);
            socket.emit("ResponseCreate", pyData.toString());
        })
    });
});
