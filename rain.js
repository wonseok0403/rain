
/** 
 *  @file       [main] rain.js, [+Requirements] VultrMaker.py
 *  @brief      우박 서버와 vultr의 작동을 도와주기위해 서버 상태 확인, 서버 구축,
 *              Vultr API 확인 등을 Socket.io 를 통해 지원하는 스크립트.
 *  @author     Wonseok. Jang
 *  @todo       Socket.io 함수를 통해 아래 구현된 함수들과 연결하여야 합니다.
 */


// 변수 설정 부분
var Connection = require('tedious').Connection;
var Request = require('tedious').Request;
var http = require('http');
var io = require('socket.io');
var server = http.createServer(function (req, res){
});

// 서버 설정 부분
server.listen(1685);
var sock = io.listen(server); 

const setServer = async () => {
    // DB 설정 부분
    const pg = require('pg');
    const connectionString = process.env.DATABASE_URL || 'postgresql://localhost:5432/';
    const client = new pg.Client(connectionString);
    await client.connect();
    var res = client.query(
        'CREATE TABLE BuildResult(app, state, date, text VARCHAR(40) not null, text VARCHAR(40) not null, text VARCHAR(40) not null)');
    await client.end();
}

setServer();

// 소켓 IO 메인 함수
sock.on("connection", function(socket){
    console.log("New-bee is here");
    // @details 
    socket.on("Ping", function(data){
        console.log("Ping!");
        socket.emit("Pong",data);
    });
    // @details  vultr에서 create를 하기 위해 필요한 dcid, vpsplanid, osid 정보를 출력합니다.
    // @return   단순하게 문자열로 RespondList 리스너에 되돌려줍니다.
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

    /*                                                                       *
    *  @details  새로운 인스턴스를 만들고 싶을 때 호출합니다.
    *  @return 
    *  @see      초기 설정을 가장 저렴하고 서버를 일본에 두고 싶다면 아래 설정을 따르십시오.
    *            {"dcid":25, "vpsplanid":201, "osid":216}                    */
    socket.on("CreateRequest", function(data){
        var ParsedData = JSON.parse(data);
        var dcid = ParsedData['dcid'];
        var vpsplanid = ParsedData['vpsplanid'];
        var osid = ParsedData['osid'];
        const {spawn} = require("child_process");
        const pyProg = spawn('python', ['./VultrMaker.py', 'create', dcid, vpsplanid, osid]);
        console.log(dcid, vpsplanid, osid);
        /**
         * @details 아래 함수는 VultrMaker.py 의 create 함수를 호출하여 호출된 내역에서 Subid를 추출합니다.
         *          주요 알고리즘은, 리턴되는 형태는 {subid : 정수값} 의 문자열 형태로, 여기서 정수값 만 추출합니다.
         */
        pyProg.stdout.on('data', function(pyData) 
        {
            console.log("pyProg 63 line is called");
            var len = pyData.toString().length;
            var ParsedData = "";
            for(var i=0; i<len; i++) {
                if(!isNaN(parseInt(pyData.toString()[i], 10))){
                    ParsedData = ParsedData + pyData.toString()[i];
                }
            }
            // 만약 해당 subid의 정수 값이 필요할 경우 아래 함수를 이용하십시오.
            //var ParsedInt = parseInt(ParsedData,10);
            //console.log("ParssedData : " + ParsedInt);

            /**
             * @details 아래 함수는 일정 간격으로 새로 생성된 인스턴스의 상태를 확인하여 running 인지 확인합니다.
             *          만약 running 상태라면 호출한 소켓에 CreateDone 리스너를 호출하여 running 임을 알립니다.
             */
            var flag = false;
            var repeat = setInterval(function(){
                const {spawn} = require("child_process");
                const pyProg = spawn('python', ['./VultrMaker.py', 'subdetail', ParsedData]);
                pyProg.stdout.on('data', function(pyData){
                    console.log(pyData.toString());
                    if( pyData.toString().indexOf('stop') > -1 ) {
                        console.log('Stop');
                        flag = true;
                    }
                    if( (pyData.toString().indexOf('run') > -1)) {
                        console.log('Running!');
                        if( flag == true) {
                            console.log('flag is true');
                            socket.emit("CreateDone", pyData.toString());
                            clearInterval(repeat);
                        }
                    }
                });
            }, 5000); // 5초(5000 ms) 간격으로 상태를 확인합니다.

            // 인스턴스의 running 여부의 상관 없이 create 에 성공했다고 알립니다.
            socket.emit("ResponseCreate", pyData.toString());
        })
    });

    /*                                                                               *
    *  @details  Vultr 계정이 보유하고있는 인스턴스들의 정보를 출력합니다.
    *  @return   ResponseServerlist 리스너에 해당 항목 정보에 대하여 문자열 형식으로 리턴합니다.    */
    socket.on("ServerList", function(data){
        const {spawn} = require("child_process");
        const pyProg = spawn('python', ['./VultrMaker.py', 'list'])
        pyProg.stdout.on('data', function(pyData){
            console.log(pyData.toString());
            socket.emit("ResponseServerList", pyData.toString());
        })
    });


});
