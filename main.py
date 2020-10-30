import subprocess
import time
#subprocess.call(r'net use m: \\192.168.16.175\nowyks /user:zps zps', shell=True)
import configparser



#ini = open('./config.ini','r')
#config =

config = configparser.RawConfigParser()
config.read('./config.ini')
litera=config.get('KONFIGURACJA','litera')
sciezka=config.get('KONFIGURACJA','sciezka')
login=config.get('KONFIGURACJA','login')
login=config.get('KONFIGURACJA','haslo')

#config.close()

while True:
    time.sleep(1)
    if subprocess.call(rf'{litera}', shell=True) == 0:
     #print("Nic sie nie dzieje")
        pass
    else:
        subprocess.call(rf'net use {litera} {sciezka}', shell=True)
        #print("Podpieto dysk")



