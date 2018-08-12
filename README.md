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
