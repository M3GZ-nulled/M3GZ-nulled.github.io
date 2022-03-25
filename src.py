import PySimpleGUI as sg
import socketio
import requests
from random import choice
from webbrowser import open
from dhooks import Webhook

sg.DEFAULT_FONT = 'Sans 11'
sg.theme('DarkTanBlue')

icon = b'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'
header = {
    #"Cookie": "nulledmember_id=4103370;io={};".format(id),
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Connection": "Upgrade",
    "Upgrade": "websocket",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Sec-WebSocket-Version": "13",
    "Sec-WebSocket-Extensions": "permessage-deflate",
    "Sec-Fetch-Dest": "websocket",
    "Sec-Fetch-Mode": "websocket",
    "Sec-Fetch-Site": "same-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}

## Auth

import os, shutil, winreg
from hashlib import sha256
from wmi import WMI
from sys import platform, exit

def get_guid():
    Registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    RawKey = winreg.OpenKey(Registry, "SOFTWARE\Microsoft\Cryptography")
    return winreg.QueryValueEx(RawKey, "MachineGuid")[0].upper()
 
def get_device_uuid():
    if platform == "linux" or platform == "linux2":
        return ""
        # linux
    elif platform == "darwin":
        return ""
        # OS X
    elif platform == "win32":
        return WMI().Win32_ComputerSystemProduct()[0].UUID
 
def calculateHWID():    
    c_name = os.environ.get("COMPUTERNAME")
    u_name = os.getlogin()
    p_rev = os.environ.get("PROCESSOR_REVISION")
    disk = shutil.disk_usage("/").total
    uuid = get_device_uuid()
    guid = get_guid()
 
    str = f"{c_name}{u_name}{p_rev}{disk}{uuid}{guid}"
    return sha256(str.encode('utf-8')).hexdigest().upper()

authkey = sg.popup_get_text('Please enter your auth key', font='Sans 11', title='Hello and welcome!', icon = icon)
if not bool(authkey): exit()

try:
    auth_register = requests.post('https://www.nulled.to/authkeys.php',
        data = {
            'register': '1',
            'key': authkey,
            'hwid': 'M3GZ' + calculateHWID(),
            'program_id': '3',
        }
    )

    a = auth_register.json()
    if a['data']['message'] in ["Succesfully registered", "Duplicate registry"]:
        auth_validate = requests.post('https://www.nulled.to/authkeys.php',
            data = {
                'validate': '1',
                'key': authkey,
                'hwid': 'M3GZ' + calculateHWID(),
                'program_id': '3',
            }
        )
        b = auth_validate.json()
        if b['status'] == True: 
            if b['data']['extra'] in ('1337', '1338'):
                sg.popup_timed('Welcome, {}!'.format(b['data']['name']), font='Sans 11', title='Hi!', icon = icon)
            else:
                sg.popup_timed('You need to be upgraded (Aqua+) to use this program!', font='Sans 11', title=':/', icon = icon)
                exit()
        elif b['status'] == False:
            if '#723' in b['data']['message']:
                sg.popup_timed('Invalid auth key!', font='Sans 11', icon = icon)
                exit()
            elif '#722' in b['data']['message']:
                sg.popup_timed('Wrong HWID', font='Sans 11', icon = icon)
                exit()
            elif '#720' in b['data']['message']:
                sg.popup_timed('Wrong program ID', font='Sans 11', icon = icon)
                exit()
            else:
                sg.popup_timed('Some unknown error occured. Please inform me about the error and how to reproduce it.', font='Sans 11', title='oops.', icon = icon)
                exit()
    else:
        sg.popup_timed('Invalid auth key!', font='Sans 11', title=':wtf:', icon = icon)
        exit()
except:
    sg.popup_timed('Unknown authentication error!', font='Sans 11', title=':wtf:', icon = icon)
    exit()


button_col = [
    [sg.B('+', size = (2,1))], [sg.B('-', size = (2,1))]
]

layout = [
    [sg.T('If any message contains:', size=(21,1)), sg.In('@{}'.format(b['data']['name']), expand_x=True, size=(40,1), key='_IN_')],
    #[sg.T('And OP has this UG:', size=(21,1)), sg.In('Nova', expand_x=True, size=(40,1))],
    [sg.T('Send it to this webhook:', size=(21,1)), sg.In('www.discord.com/webhook/dQw4w9WgXcQ', expand_x=True, size=(40,1), key='_WBHK_')],
    [sg.T('And reply with a random message from:', size=(21,2)), sg.Listbox(key='_LIST_', values=['Hello', 'Gib @M3GZ coder ug ty'], expand_x=True, size=(None, 4)), sg.Col(button_col)], #sg.In('Hello', expand_x=True, size=(40,1))],
    [sg.T()],
    [sg.P(), sg.B('Create Bot', size=(9,1), key='_CREATE_'),sg.B('Stop Bot', size=(9,1), disabled=True, key='_STOP_'), sg.B('About', size=(9,1)), sg.P()]
]

w = sg.Window('ShoutBot by M3GZ (coder ug when kappo)', layout, font=('Sans', 11), icon = icon)

while True:
    event, values = w.read()
    if event == sg.WIN_CLOSED:
        try: sio.disconnect()
        except: pass
        break
    if event == 'About':
        popup_window = sg.Window('About Program (coder ug when :pepe:)', [[sg.T('Nulled Memebox User Bot v1.0')], [sg.T('Made by'), sg.T('M3GZ', text_color='cyan', enable_events=True, key='_M1_', font='sans 10 underline'), sg.T('(click to support me)', enable_events=True, key='_M2_')], [sg.T('~ 19th March, 2022')], [sg.T('Auto-reply is dangerous and I\'ve been sb banned for 24 hours\nbecause people were abusing it before kekw\nUse with caution, I\'m not responsible\n\nBtw if you do "!meme" or "!sb x" (x is a number) in sb, it should\ntrigger my selfbot to post a random meme from reddit\nand to screenshot the last x sb messages respectively\n\nPS good luck to all those participating in the coding event!')], [sg.B('Close', size=(5,1))]], modal = True, font="Sans 11", icon = icon)
        while True:
            e, v = popup_window.read()
            if e in ['Close', sg.WIN_CLOSED]: break
            if e.startswith('_M'):open('https://www.nulled.to/reputation.php?uid=4103370')
        popup_window.close()
    if event == '+':
        w['_LIST_'].update(w['_LIST_'].Values + [sg.popup_get_text('Enter new phrase - ', title='New phrase', font='Sans 11', icon = icon)])
    if event == '-':
        try:
            w['_LIST_'].update([x for x in w['_LIST_'].Values if x != values['_LIST_'][0]])
        except IndexError: pass
    if event == '_STOP_':
        w['_CREATE_'].update(disabled=False)
        w['_STOP_'].update(disabled=True)
        sio.disconnect()
    if event == '_CREATE_':
        w['_CREATE_'].update(disabled=True)
        w['_STOP_'].update(disabled=False)
        sessid = sg.popup_get_text('Enter your session iD:', font='Sans 11', icon = icon)
        try:
            hook = Webhook(values['_WBHK_'])
            hook.send('Nulled SB monitoring started')
        except ValueError:
            sg.popup_timed('Invalid webhook URL! Messages won\'t be sent.', title='Error :monkas:', font='Sans 11', icon = icon)
        sio = socketio.Client(reconnection_delay=0)
        sio.connect('wss://chat-ssl2.nulled.to'.format(id), header, transports=['websocket'], wait_timeout = 10)
        sio.emit("authenticate", {"token":sessid})
        sio.emit("subscribe", {"channelName": "general"})

        @sio.on('connect')
        def connect_handler():
            sio.emit("authenticate", {"token":sessid})
            sio.emit("subscribe", {"channelName": "general"})

        @sio.on('message')
        def handler(data):
            try:
                a = data['data']['message']
                if values['_IN_'].lower() in a['text'].lower():
                    try:
                        hook.send("{} said: {}".format(a['user']['username'], a['text']))
                    except: pass
                    try:
                        sio.emit("message", {"channelName":"general","text":choice(w['_LIST_'].Values)})
                    except: pass
            except Exception as e:
                pass
