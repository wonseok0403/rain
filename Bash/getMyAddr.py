import netifaces as ni
ni.ifaddresses('ens3')
ip = ni.ifaddresses('ens3')[ni.AF_INET][0]['addr']
print(ip)
