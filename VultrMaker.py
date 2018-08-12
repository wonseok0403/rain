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
    print(Vultr.server.list())

def CheckStatusById(Subid) :
    print(Vultr.server.list(subid=Subid)['power_status'])
    

if __name__ == '__main__':
    if( len( sys.argv ) < 2 ):
        print('옵션을 정의해야 합니다.')
        print('지원하는 옵션 ---------------------- *')
        print(' -- 1. create [dicd] [vpsplanid] [osid] ')
        print(' -- 2. list ')
        print((' -- 3. listall (dcid, osid, vpsplanid 확인)'))
        print(' -- 4. subdetail [Subid] ')
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
