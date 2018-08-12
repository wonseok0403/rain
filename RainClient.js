/** 
 *  @file       [main] RainClient.js, [Configure] .RainClientConfigure
 *  @brief      API 를 통해 유저와 소통하여 rain.js 의 소켓 함수들과 통신하는 프로그램.
 *              예를 들어 유저가 새로운 클라우드를 만들고 싶다면, API 를 통해 이 프로그램에 요청하고,
 *              프로그램은 socket.io 를 통해 rain.js 에 해당 요청을 전달한 후, 서버 구축이 완료되면 이 프로그램의 리스너를 호출한다.
 *  @author     Wonseok. Jang
 *  @todo       유저는 이 프로그램을 도커 시스템에 실행시켜야 합니다.
 */

// 전역 변수 선언 부분
// 프로그램을 다른 프로그램에서 이용할 수 있도록, Rain.js와의 연동되는 내역을 전역변수로 정의한다.
global.port = 0; 
global.host = "";
global.socket = null;

// 프로그램을 본격적으로 시작하기 전, Rain 서버의 설정을 읽어오는 부분.
// 서버 설정 read는 비동기적으로 구성된다.
var lineReader = require('readline').createInterface({
    input: require('fs').createReadStream('.RainClientConfigure')
  });
lineReader.on('line', function (line) {
    var arrayOfString = line.split(' ');
    var method = arrayOfString[0];
    var way = arrayOfString[1];
    if( method == 'HOST') {
        global.host = way;
    }
    if( method == 'PORT') {
        global.port = way;
    }
    if( global.port != 0 && global.host != "") {
        global.socket = io.connect('http://'+global.host+":"+global.port, {reconnect: true});
    }
  });


// Restful API 를 운영하기 위한 웹서버 구축 부분
const express = require('express');
const bodyparser = require('body-parser');
const app = express();
const io = require('socket.io-client');
// 웹서버에서 post message 를 body 로 부터 파싱하기 위한 과정 ( 어떤 브라우저에서든 사용 가능하도록 설정 )
app.use(bodyparser.urlencoded({
    extended: true
}));
app.use(bodyparser.json());
// !- Restful API 구축 부분 !- //
// 명명 규칙에 대해서는 https://restfulapi.net/resource-naming/ 문서를 참고하십시오.

// [GET] /
// @details     API 프로그램의 작동 상황을 점검하고, rain.js 와 소켓을 바인딩합니다.
app.get('/', function(req, res){
    console.log("루트 디렉터리 호출");
    global.socket.on("Pong", function(data){
        console.log("Pong!");
        res.json(data);
    })
    global.socket.emit("Ping", {date: new Date()})
});

// [GET] /list/instances
// @details     Vultr 에 등록된 인스턴스들의 정보를 열람하기 위해 호출한다.
// @return      json 형식으로 리턴된다.
app.get('/list/instances', function(req, res){
    console.log("/list/instances 함수 호출");
    global.socket.on("ResponseServerList", function(data){
        res.json(data);
        res.status(200);
    });
    global.socket.emit("ServerList", {});
});

// [GET] /list/vultr-lists
// @details     Vultr 에서 vm create 를 위해 필요한 여러 id 값의 정보를 호출한다.
// @return      dcid, vpsplanid, osid 순서로 모든 항목을 리턴한다.
// @note        각각 25, 201, 216 일때 서버가 일본에 있으며, 50GB SSD, 1TB BW를 제공받는다.
app.get('/list/vultr-lists', function(req, res){
    console.log("/list/vultr-lists 함수 호출");
    global.socket.on("RespondList", function(data){
        console.log(data);
    });
    global.socket.emit("List", {});
});

/** [POST] /server/instance
 *  @details    Vultr에서 새로운 인스턴스를 생성합니다.
 *  @param      body 에서 dcid, vpsplanid, osid 에 값을 넣어서 post 메시지를 보내주어야 합니다.
 *  @return     생성 상태가 확인되면 ResponseCreate 함수가 호출되고 해당 SubID 를 Return 합니다.
 *              새로 생성된 인스턴스의 상태가 running이 되면 CreateDone 리스너가 호출됩니다. */
app.post('/server/instance', function(req, res){
    console.log(req.body);
    var dcid = req.body.dcid;
    var vpsplanid = req.body.vpsplanid;
    var osid = req.body.osid;
    var Parameter = '{' 
                    + '"dcid" : ' + dcid + ","
                    + '"vpsplanid" : ' + vpsplanid + ","
                    + '"osid" : ' + osid 
    + '}';
    
    // 생성된 인스턴스 상태가 running 일 경우 호출됩니다.
    global.socket.on("CreateDone", function(data){
        res.json(data.toString());
        console.log("인스턴스 실행 상황 확인");
    });
    // 인스턴스 생성 요청이 완료되었을 경우 호출됩니다.
    global.socket.on("ResponseCreate", function(data){
        console.log("인스턴스 생성 완료 : " , data.toString());
        console.log("인스턴스 실행 대기중");
    });
    global.socket.emit("CreateRequest", Parameter);
});

 // !- Webserver 가동 부분 !- //
app.listen(3000, () => {
    console.log("Rain Client is running on 3000 !!!");
});
