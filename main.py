import subprocess
import time
import configparser
import json
import socket
import win32wnet
import win32net

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

config = configparser.RawConfigParser()
config.read('./config.ini')
litera=config.get('KONFIGURACJA','litera')
sciezka=config.get('KONFIGURACJA','sciezka')
login=config.get('KONFIGURACJA','login')
login=config.get('KONFIGURACJA','haslo')
a=[]

while True:
    time.sleep(1)
    f = open('config.json', 'r')
    sciezki = json.load(f)
    adres = ""

    for y in sciezki['uzytkownicy']:
        if y["adres_ip"] == host_ip:
            adres = y["adres_ip"]
            dyski = y["litery"]

    f.close()

    (_drives, total, resume) = win32net.NetUseEnum(None, 0)
    for drive in _drives:
        if drive['local'] and drive['local'][0].lower()!=litera[0] and drive['local'][0].lower()!="g":
            a.append(drive['local'][0].lower())

    if subprocess.call(rf'{litera}', shell=True) == 0:

        if host_ip==adres:
            for d in dyski:
                if d in a:
                    a.remove(d)
            for temp in a:
                subprocess.call(rf'net use {temp}: /delete', shell=True)
            for d in dyski:
                # print(d)
                for x in sciezki["sciezki"]:
                    # print(d,x)
                    if d == x[0]:
                        # print(1,d,x)
                        if subprocess.call(rf'{d}:', shell=True) == 0:
                            if x[1:] == win32wnet.WNetGetConnection(f'{d}:'):
                                pass
                            else:
                                subprocess.call(rf'net use {d}: /delete', shell=True)
                                time.sleep(15)
                                subprocess.call(rf'net use {d}: {x[1:]}', shell=True)

                        else:
                            subprocess.call(rf'net use {d}: {x[1:]}', shell=True)
                    else:
                        pass
            else:
                pass  # jesli adres sie nie zgadza nic nie robi
    else:
        subprocess.call(rf'net use {litera} {sciezka}', shell=True)
    a=[]
