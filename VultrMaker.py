# -*- coding: utf-8 -*-
import tests
import vultr
import unittest
import os, subprocess, sys
from pexpect import pxssh


# 벌터 초기 설정 시작 --------------------------------
# 벌터 API key 불러오기
keyFile = open('./.config', 'r')
line = keyFile.readlines()
API_KEY = ""
for i in line :
    ParsedLine = i.split('=')
    # apikey 일 경우 vultr의 api임에 유의한다.
    method = ParsedLine[0]
    if( method == "apikey" ) :
        API_KEY = ParsedLine[1].strip()
        os.putenv("VULTR_KEY",API_KEY)       # 환경변수 등록
        #os.system("echo $VULTR_KEY")        # 프로그램이 실행되지 않으면 이 라인을 확인하십시오.
        Vultr = vultr.Vultr(API_KEY)         # 벌터 API 등록
        
# 벌터 초기 설정 종료 ----------------------------------- *
def Create(dcid, vpslanid, osid):
    return Vultr.server.create(dcid, vpslanid, osid)
    #return "{u'SUBID': u'17910597'}"
def ListAll() :
    # 서버 리스트가 아님에 주의하십시오.
    print( GetDcids() )
    print('\n\n')
    print(GetVPSPIDs())
    print('\n\n')
    print(GetOSIDs())

def GetDcids() :
    # 25 = 도쿄
    return Vultr.regions.list()

def GetVPSPIDs() :
    # 201 1024MB ram, 25GB SSD, 1.0TB BW, price per 5
    return Vultr.plans.list()

def GetOSIDs() :
    # 216 ubuntu 16.04 i386
    return Vultr.os.list()

def GetInstances() :
    # 서버 리스트 항목을 리턴합니다.
    print(Vultr.server.list())

def CheckStatusById(Subid) :
    print(Vultr.server.list(subid=Subid)['power_status'])
    
def GetSubidByName(name):
    # Vultr.server.list 함수는 사용자의 인스턴스 목록을 { subid : { isntance detail } } 와 같은 형식으로 리턴합니다.
    # 이렇게 리턴된 인스턴스 내역에서 서버 라벨 정보를 비교합니다.
    ServerList = Vultr.server.list()
    #print(ServerList)
    for i in ServerList :
        if( ServerList[i]['label'] == name ) :
            return i
    return 0

def SystemInit(Subid) :
    # 4. 폴링을 통해서 서버가 올라갔다고 확인이 되면, 서버의 기본 root 비밀번호로 그 서버에 접속한다.
    ## Get IP, Username[root], PW
    ServerList = Vultr.server.list()
    SERV_IP = ""
    USER_NAME = "root"
    USER_PW = ""
    for i in ServerList : 
        if( ServerList[i]['SUBID'] == Subid) :
            SERV_IP = ServerList[i]['main_ip']
            USER_PW = ServerList[i]['default_password']
            break
    Shell = pxssh.pxssh()
    Shell.login(SERV_IP, USER_NAME, USER_PW)
    Shell.sendline('git clone https://github.com/wonseok0403/RainAutoscript.git')
    Shell.sendline("chmod +x ./RainAutoscript/AutoScript.sh")
    Shell.sendline("./RainAutoscript/AutoScript.sh")
    Shell.prompt()
    print(Shell.before.decode())

    # 5. 새로운 클라우드 인스턴스에 passwd, update, upgrade, 랜처 호스트 등록을 한다.
    # 6. 새로운 서버에서 avocado-test-server 깃허브 리포를 clone한다.
    # 7. 금방 클론한 리포에서 docker-compose up -d --build하여 코드를 배포시킨다.

    # 5-7 의 모든 과정이 위 레포지토리에 들어있다.

def SetServer(ip, role, pw) :
    # 4. 폴링을 통해서 서버가 올라갔다고 확인이 되면, 서버의 기본 root 비밀번호로 그 서버에 접속한다.
    ## Get IP, Username[root], PW
    ServerList = Vultr.server.list()
    SERV_IP = ip
    USER_NAME = role
    USER_PW = pw

    Shell = pxssh.pxssh()
    Shell.login(SERV_IP, USER_NAME, USER_PW)
    Shell.sendline('git clone https://github.com/wonseok0403/RainAutoscript.git')
    Shell.sendline("chmod +x ./RainAutoscript/AutoScript.sh")
    Shell.sendline("./RainAutoscript/AutoScript.sh")
    Shell.prompt()
    print(Shell.before.decode())

    # 5. 새로운 클라우드 인스턴스에 passwd, update, upgrade, 랜처 호스트 등록을 한다.
    # 6. 새로운 서버에서 avocado-test-server 깃허브 리포를 clone한다.
    # 7. 금방 클론한 리포에서 docker-compose up -d --build하여 코드를 배포시킨다.

def GetIPbySubid(subid) :
    ServerList = Vultr.server.list()
    #print(ServerList)
    for i in ServerList :
        if( ServerList[i]['SUBID'] == subid ) :
            print ServerList[i]['main_ip']
            return
    print 0

if __name__ == '__main__':
    if( len( sys.argv ) < 2 ):
        print('옵션을 정의해야 합니다.')
        print('지원하는 옵션 ---------------------- *')
        print(' -- 1. create [dicd] [vpsplanid] [osid] ')
        print(' -- 2. list ')
        print((' -- 3. listall (dcid, osid, vpsplanid 확인)'))
        print(' -- 4. subdetail [Subid] ')
        print(' -- 5. gsn [Name] (Get Subid by Name) [testing] ')
        print(' -- 6. sysinit [Subid] ')
        print(' -- 7. setserver [ip] [role] [pw]')
        print(' -- 8. subtoip [subid] ')
        print('-------------------------------------')
    option = sys.argv[1]
    if( option == 'list' ) :
        # vultr instance 리스트 출력하기
        print( GetInstances() )
    if( option == 'listall' ) :
        ListAll()

    if( option == 'create' ) :
        if( len( sys.argv ) < 5 ) :
            print('태그명을 입력해야합니다. ( create <tag> )')
        else :
            print(Create(sys.argv[2], sys.argv[3], sys.argv[4]))
    if( option == 'subdetail' ) :
        CheckStatusById(sys.argv[2])
    if( option == 'gsn' ):
        tmp = GetSubidByName(sys.argv[2])
        print( tmp ) 
    if( option == 'sysinit' ):
        SystemInit( sys.argv[2] )
    if( option == 'setserver' ) :
        SetServer( sys.argv[2], sys.argv[3], sys.argv[4])
    if( option == 'subtoip' ) :
        GetIPbySubid( sys.argv[2] )
