import requests,urllib.request,socket,PySimpleGUI as sg,threading, pyperclip, pyglet
from webbrowser import open as web
from datetime import datetime

pyglet.font.add_file('.\\visby.otf')
font = 'visby 12'

sg.theme('DarkBlue17')

keep_checking = False

def divide_chunks(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def is_bad_proxy(typ, ips, window):
    global keep_checking
    for pip in ips:
        if not keep_checking: return
        try:
            proxy_handler = urllib.request.ProxyHandler({typ:pip})
            opener = urllib.request.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            sock=urllib.request.urlopen(typ+'://www.google.com')
        except urllib.error.HTTPError:
            window.write_event_value('_JOIN_BAD_', None)
            continue
        except Exception:
            window.write_event_value('_JOIN_BAD_', None)
            continue
        window.write_event_value('_JOIN_GOOD_'+pip, None)

def create_window():
    global keep_checking
    speeds = {1:'All', 2:'Slow', 3:'Medium', 4:'Fast'}
    protocols = {0:'http', 1:'https', 2:'socks4', 3:'socks5', 4:'http', 5:'https'}

    lay_get = [
        [sg.T('Country Code:'), sg.In('All', size=(4,1), key='_CONT_'), sg.T('Anonimity:'), sg.Combo(['All', 'Elite', 'Anonymous', 'Transparent'], 'All', size=(12,1), key='_ANON_', readonly=True)],
        [sg.T('Protocol:'), sg.Radio('HTTP','_PROTORAD_'), sg.Radio('HTTPS','_PROTORAD_',default=True), sg.Radio('SOCKS4','_PROTORAD_'), sg.Radio('SOCKS5','_PROTORAD_')],
        [sg.T('Speed:'), sg.Slider((1,4), size=(20,10), orientation='h', disable_number_display=True, expand_x=True, enable_events=True, key='_SPEED_'),sg.T(' All', size=(8,1), relief=sg.RELIEF_SUNKEN, key='_SPEED_SHOW_')],
        [sg.T('  '), sg.B('Get Free Proxies!', key='_GET_',size=(20,1)), sg.P(), sg.T('Total Proxies:    '), sg.T(' 1', relief=sg.RELIEF_SUNKEN, key='_LEN_', size=(6,1)), sg.P()],
        [sg.T('  '), sg.B('Export To Text File', key='_GET_EXPORT_', size=(20,1)), sg.P(), sg.B('Copy To Clipboard', key='_GET_COPY_',size=(20,1)),sg.P()],
        [sg.Multiline('127.0.0.1 :monkas:', key='_PROX_SHOW_', size=(20,10), expand_x=True)]
    ]

    lay_chk = [
        [sg.T('Protocol:'), sg.Radio('HTTP','_CHECKRAD_'), sg.Radio('HTTPS','_CHECKRAD_',default=True), sg.P(), sg.T('Timeout (sec):'), sg.Spin([i for i in range(1,999)], initial_value=5, key='_TIME_', size=(5,1))],
        [sg.T('Bots:'), sg.Spin([i for i in range(1,200)], initial_value=200, key='_BOTS_', size=(5,1)), sg.P(), sg.B('Start Checking', key='_CHECK_', size=(15,1)), sg.B('Stop Checking', key='_STOP_CHECK_', disabled=True, size=(15,1))],
        [sg.B('Export To Text File', size=(23,1), key='_CHK_EXPORT_'), sg.P(), sg.B('Copy To Clipboard', size=(23,1), key='_CHK_COPY_')],
        [sg.T('Good:'), sg.T(' 0', relief=sg.RELIEF_SUNKEN, key='_LEN_WORK_', size=(6,1)),sg.T(), sg.T('Bad:'), sg.T(' 0', relief=sg.RELIEF_SUNKEN, key='_LEN_BAD_', size=(6,1)), sg.T(), sg.ProgressBar(100, orientation='h', size=(1, 10), key='progressbar', expand_x=True)],
        [sg.Multiline('Paste Proxies Here', size=(20,10), expand_x = True, expand_y = True, key='_CHK_PROX_')]
    ]

    lay_abt = [
        [sg.T('\n\n\n\nPr0x4all - Free Proxy Scraper (v1.0)')],
        [sg.T('Created by'), sg.T('M3GZ', text_color='cyan', enable_events=True, key='_M2_', font=font+' underline')],
        [sg.T()],
        [sg.B('See my other releases!', key='_R_', size=(30,1))],
        [sg.B('Visit my profile!', key='_M1_', size=(30,1))],
    ]

    lay = [
        [sg.TabGroup(
            [[sg.Tab('Get Proxies', lay_get), sg.Tab('Check Proxies', lay_chk), sg.Tab('About Program', lay_abt, element_justification='c')]]
        )],
    ]

    total = 0
    w = sg.Window('Pr0x4all - Proxy Tool by M3GZ', lay, font=font, icon='.\icon.ico')

    while True:
        e,v = w.read()
        if e == sg.WIN_CLOSED: break
        if e == '_SPEED_': w['_SPEED_SHOW_'].update(' '+speeds[v[e]])
        if e == '_GET_':
            
            protocol = protocols[[x for x in [0,1,2,3] if v[x] == True][0]]
            url_proxyscrape = 'https://api.proxyscrape.com/v2/?request=displayproxies'
            url_geonode = 'https://proxylist.geonode.com/api/proxy-list?limit=500'
            
            if protocol[:-1] == 'socks': url_proxyscrape += '&protocol='+protocol
            elif protocol == 'https': url_proxyscrape += '&protocol=http&ssl=yes'
            elif protocol == 'http': url_proxyscrape += '&protocol=http&ssl=no'
            
            if v['_SPEED_'] == 4: url_proxyscrape += '&timeout=500'
            if v['_SPEED_'] == 3: url_proxyscrape += '&timeout=1500'
            if v['_SPEED_'] == 2: url_proxyscrape += '&timeout=5000'
            if v['_SPEED_'] == 1: url_proxyscrape += '&timeout=10000'

            url_proxyscrape += '&country='+v['_CONT_'].lower()
            url_proxyscrape += '&anonymity='+v['_ANON_'].lower()

            url_geonode += '&protocols='+protocol
            if v['_SPEED_'] != 1: url_geonode += '&speed='+speeds[v['_SPEED_']].lower()
            if v['_CONT_'].lower() != 'all': url_geonode += '&country='+v['_CONT_'].lower()
            if v['_ANON_'] != 'All': url_geonode += '&anonymityLevel='+v['_ANON_'].lower()

            prox_gn = requests.get(url_geonode).json()['data']
            proxies = ('\n'.join(['{}:{}'.format(x['ip'], x['port']) for x in prox_gn]) + '\n' + requests.get(url_proxyscrape).text).strip()
            w['_LEN_'].update(' {}'.format(len(proxies.split())))
            w['_PROX_SHOW_'].update(proxies)
            print(url_geonode, url_proxyscrape)
        if e.startswith('_M'): web('https://www.nulled.to/user/4103370-m3gz')
        if e == '_R_': web('https://www.nulled.to/topic/1308515-list-of-releases/')

        if e == '_STOP_CHECK_':
            keep_checking = False
            w['_STOP_CHECK_'].update(disabled= True)

        if e == '_CHECK_':
            w['_STOP_CHECK_'].update(disabled=False)
            keep_checking = True

            w['_LEN_BAD_'].update(' 0')
            w['_LEN_WORK_'].update(' 0')

            socket.setdefaulttimeout(int(v['_TIME_']))
            protocol = protocols[[x for x in [4,5] if v[x] == True][0]]
            w['_CHK_PROX_'].update('Working proxies:')
            
            ips = v['_CHK_PROX_'].strip().split()
            total = len(ips)
            if total<=int(v['_BOTS_']):
                threads = []
                for item in ips:
                    threads.append(threading.Thread(target=is_bad_proxy, args=(protocol, [item], w), daemon=True))
                for i in threads: i.start()
            else:
                for i in divide_chunks(ips, int(v['_BOTS_'])):
                    threading.Thread(target=is_bad_proxy, args=(protocol, i, w), daemon=True).start()

        if e == '_GET_COPY_': pyperclip.copy(v['_PROX_SHOW_'])
        if e == '_GET_EXPORT_':
            with open('prox4all_{}.txt'.format(datetime.now().strftime("%d%m%Y-%H%M%S")), 'w') as f:
                f.write('{} Proxies\nScraped by Pr0x4all by M3GZ\nOn {}\n\n'.format(protocols[[x for x in [0,1,2,3] if v[x] == True][0]], datetime.now().strftime("%d/%m/%Y-%H:%M:%S")) + v['_PROX_SHOW_'])
        if e == '_CHK_COPY_': pyperclip.copy(v['_CHK_PROX_'])
        if e == '_CHK_EXPORT_':
            with open('prox4all_{}.txt'.format(datetime.now().strftime("%d%m%Y-%H%M%S")), 'w') as f:
                f.write('{} Proxies\nScraped by Pr0x4all by M3GZ\nThese have been checked and confirmed to be working\nOn {}\n\n'.format(protocols[[x for x in [4,5] if v[x] == True][0]], datetime.now().strftime("%d/%m/%Y-%H:%M:%S")) + v['_CHK_PROX_'])

        if e == '_JOIN_BAD_':
            w['_LEN_BAD_'].update(int(w['_LEN_BAD_'].get()) + 1)
            a = ((int(w['_LEN_BAD_'].get()) + int(w['_LEN_WORK_'].get())) / total)*100
            w['progressbar'].update( a )

        if e.startswith('_JOIN_GOOD_'): 
            w['_LEN_WORK_'].update(int(w['_LEN_WORK_'].get()) + 1)
            w['_CHK_PROX_'].update(w['_CHK_PROX_'].get() + '\n' + e[11:])
            a = ((int(w['_LEN_BAD_'].get()) + int(w['_LEN_WORK_'].get())) / total)*100
            #w['progressbar'].update( 100 if a>70 else a )
            w['progressbar'].update( a )
    
    w.close()

if __name__ == '__main__': create_window()
