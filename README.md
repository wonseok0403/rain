# Rain
### Rain 은 우박 서버가 로드밸런싱을 하는 과정에서 vultr 에 서버 생성을 요청하고, 요청된 내역이 인가되어 생성된 서버가 running 상태가 되는지 체크하는지 확인하도록 구축되었습니다. Rain 서버는 Rain-Client 와 함께 작동합니다.

![2018-08-12 5 32 43](https://user-images.githubusercontent.com/20366503/44000274-eaf62e06-9e57-11e8-9419-534f6a1da3c8.png)

# VultrMaker.py
### Rain server 는 독립적으로 Vultr API 와 소통하지 않습니다. 비동기 요청을 모두 받아 따로 처리하기위해 파이썬 스크립트로 실제 API 개발 내역이 구성되어 있습니다. 다음은 VultrMaker 에서 지원하는 함수의 목록과 설명 입니다.

* Create(dcid, vpsplanid, osid)
서버 구축을 위한 함수. Vultr 에서는 새로운 인스턴스를 생성하기 위해 dcid, vpsplanid, osid 를 필요로 합니다. 여기서 각각 서버가 구축될 지역 id, 미리 정의된 서버 스펙 id, 미리 정의된 운영 체제 목록 id 입니다. 이 정보를 인자로 넣어주어야 인스턴스가 생성되며 {'SUBID': '<정수 값>'} 의 형태의 SUBID 값이 리턴됩니다. 

* ListAll()
서버 구축을 위해 필요한 dcid, vpsplanid, osid 정보를 출력합니다. 각각 개행 문자를 통해 구분되어 리턴되며, 사용자는 이 함수를 통해 vultr 에서 제공하는 서버 구성 형태를 살펴볼 수 있습니다.

* GetDcids(), GetVPSPIDs(), GetOSIDs()
ListAll 함수에서 호출하기 위해 만들어진 함수입니다. 파이썬 스크립트를 수정하여 필요한 내역만 얻고 싶다면 이 함수들을 이용하십시오.

* GetInstances()
사용자가 보유하고 있는 가상머신 인스턴스들 목록의 정보를 출력합니다. 각 목록의 인스턴스 정보는 현재 상태( Stopped, Starting, Running, Destroying ), SUBID 등 으로 구성됩니다. 

* CheckStatusById(Subid)
해당 파라미터 값을 Subid 로 갖는 인스턴스의 상태를 확인하여 리턴합니다. Stopped, Starting, Running, Destroyng 으로 구성됩니다.

### Vultr Maker 실행하기
#### 요구 사항 설치
> pip install -r requirements.txt
#### API 값 넣어주기
> vim .config
> apikey=< apikey 값 from vultr > // <-- 입력
##### 1) 클라우드 생성하기
> python ./VultrMaker create [dcid] [vpsplanid] [osid]
##### 2) Vultr 계정에 포함된 모든 인스턴스 목록 보기
> python ./VultrMaker list
##### 3) Vultr 에서 제공하는 dcid, vpsplanid, osid 목록 보기
> python ./VultrMaker listall
##### 4) 해당 Subid 를 subid 값으로 갖는 인스턴스의 상태 살펴보기
> python ./VultrMaker subdetail [Subid]

# Rain.js
### Rain.js 는 Rain 서버 입니다. Rain-Client 는 Rain-client 에 API 를 호출하면 등록된 Rain-Server 에서 소켓 처리 함수를 호출하여 처리를 시작합니다. Rain-Client 는 우박에 장착되어 적절히 처리될 수 있으며 단 한개의 Rain-Server 와 통신하며 Vultr 처리는 각각의 비동기 함수들이 따로 파이썬 스크립트를 실행하여 처리합니다.

다음은 Rain.js 에 구현된 소켓 함수의 바인딩 함수와 호출하는 리스너 함수의 설명입니다.

* connection( socket )
소켓이 바인딩되면 자동으로 처음에 호출됩니다. 바인딩된 소켓의 정보는 파라미터 'socket' 에 있습니다.

* Ping( data ) - Listener ( Pong(data) )
클라이언트가 서버와의 접속 상태를 확인하고 싶을 때 호출합니다. 넘어온 데이터 (파라미터) 의 값을 그대로 emit 합니다.

* List( data ) - Listener ( RespondList( pyData ) ) 
벌터에서 제공하는 dcid, vpsplanid, osid 목록을 출력합니다. 파이썬 스크립트에 데이터를 요청하여 문자열로 변환한 후 RespondList를 emit 하여 데이터를 송신합니다. 

* CreateRequest( data ) - Listener ( CreateDone( pyData.toString() ), ResponseCreate( pyData.toString() )
새로운 가상머신을 구축하도록 요청합니다. 이 요청은 파이썬 스크립트로 전달되고 벌터 API로 연결됩니다. 이 API가 호출되고, 일단 벌터 인스턴스 생성이 완료되면 응답 메시지가 오게됩니다. 이 응답메시지는 Subid 의 값이며 ResponseCreate 함수 파라미터 안에 들어갑니다.
새로 생성된 인스턴스의 상태는 running( 기존에 있던 클라우드 제거작업 ) -> stopped( 새로운 운영체제 설치 ) -> starting( 운영체제 설치 완료 후 전원 ) -> running( 작동 ) 의 상태를 거치게 됩니다. stopped 를 거치고, running 상태가 되면 CreateDone 함수를 호출하여 생성 완료를 알리게 됩니다.

* ServerList( data ) - Listener ( ResponseServerList( pyData.toString() ) 
벌터 계정이 가지고 있는 모든 서버 리스트를 리턴합니다. API호출이 완료도면 해당 내역을 문자열로 변환하여 리스너에 파라미터로 넘겨줍니다.  

#### CreateRequest 부분은 Rain.js 의 존재 이유이기도 하며 굉장이 중요한 함수입니다. 이 함수의 구조도는 다음과 같습니다.
