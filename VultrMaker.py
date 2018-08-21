# -*- coding: utf-8 -*-
import tests
import vultr
import unittest
import os, subprocess, sys


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

if __name__ == '__main__':
    if( len( sys.argv ) < 2 ):
        print('옵션을 정의해야 합니다.')
        print('지원하는 옵션 ---------------------- *')
        print(' -- 1. create [dicd] [vpsplanid] [osid] ')
        print(' -- 2. list ')
        print((' -- 3. listall (dcid, osid, vpsplanid 확인)'))
        print(' -- 4. subdetail [Subid] ')
        print(' -- 5. gsn [Name] (Get Subid by Name) [testing] ')
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
