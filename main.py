import subprocess
import time
import configparser
import json
import socket
import win32wnet
import win32net

config = configparser.RawConfigParser()
config.read('./config.ini')
litera=config.get('KONFIGURACJA','litera')
sciezka=config.get('KONFIGURACJA','sciezka')
login=config.get('KONFIGURACJA','login')
haslo=config.get('KONFIGURACJA','haslo')

while True:
    time.sleep(1)
    a = []
    f = open('config.json', 'r')
    sciezki = json.load(f)
    adres = ""

    for y in sciezki['uzytkownicy']:
        if y["adres_ip"] == socket.gethostbyname(socket.gethostname()):
            adres = y["adres_ip"]
            dyski = y["litery"]

    f.close()

    (_drives, total, resume) = win32net.NetUseEnum(None, 0)
    for drive in _drives:
        if drive['local'] and drive['local'][0].lower()!=litera[0] and drive['local'][0].lower() != "g":
            a.append(drive['local'][0].lower())

    if subprocess.call(rf'{litera}', shell=True) == 0:
        if socket.gethostbyname(socket.gethostname()) == adres:
            for d in dyski:
                if d in a:
                    a.remove(d)
            for temp in a:
                subprocess.call(rf'net use {temp}: /delete', shell=True)
            for d in dyski:
                for x in sciezki["sciezki"]:
                    if d == x[0]:
                        if subprocess.call(rf'{d}:', shell=True) == 0:
                            if x[1:] != win32wnet.WNetGetConnection(f'{d}:'):
                                subprocess.call(rf'net use {d}: /delete', shell=True)
                                time.sleep(15)
                                subprocess.call(rf'net use {d}: {x[1:]}', shell=True)
                        elif subprocess.call(rf'net use {d}: {x[1:]}', shell=True) != 0:
                                for k in sciezki["hasla"]:
                                    subprocess.call(rf'net use {d}: {x[1:]} /user:%s %s'
                                                    % (k[f"{d}"].split(':')[0],
                                                       k[f"{d}"].split(':')[1]), shell=True)
    elif subprocess.call(rf'net use {litera} {sciezka}', shell=True) != 0:
        subprocess.call(rf'net use {litera} {sciezka} /user:{login} {haslo}', shell=True)

