from pystyle import Colors, Colorate, Write
from colorama import Fore
import threading
import requests
import time
import random

print(Colorate.Horizontal(Colors.cyan_to_blue, (r'''
 ▄▄▄       ▄████▄   ▒█████   ██▀███   ███▄    █ ▒███████▒
▒████▄    ▒██▀ ▀█  ▒██▒  ██▒▓██ ▒ ██▒ ██ ▀█   █ ▒ ▒ ▒ ▄▀░
▒██  ▀█▄  ▒▓█    ▄ ▒██░  ██▒▓██ ░▄█ ▒▓██  ▀█ ██▒░ ▒ ▄▀▒░ 
░██▄▄▄▄██ ▒▓▓▄ ▄██▒▒██   ██░▒██▀▀█▄  ▓██▒  ▐▌██▒  ▄▀▒   ░
 ▓█   ▓██▒▒ ▓███▀ ░░ ████▓▒░░██▓ ▒██▒▒██░   ▓██░▒███████▒
 ▒▒   ▓▒█░░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ▒░   ▒ ▒ ░▒▒ ▓░▒░▒
  ▒   ▒▒ ░  ░  ▒     ░ ▒ ▒░   ░▒ ░ ▒░░ ░░   ░ ░░░░▒ ▒ ░ ▒
  ░   ▒   ░        ░ ░ ░ ▒    ░░   ░    ░   ░ ░ ░ ░ ░ ░ ░
      ░  ░░ ░          ░ ░     ░              ░   ░ ░    
          ░                                     ░                              

[1] Token Spammer          [3] Webhook Spammer          [5] Proxy Gen
[2] Token Checker          [4] Bot Nuke                 [6] Ip Info             [7] Info
                                                ''')))

opt = Write.Input('Sbirro > ', Colors.blue_to_cyan)

try:
    opt = int(opt)
except ValueError:
    print(Fore.LIGHTRED_EX + "Invalid input! Please restart and enter a valid number (1-6).")
    exit()

def get_proxy():
    url = 'https://www.proxy-list.download/api/v1/get?type=https'
    try:
        response = requests.get(url)
        proxies = response.text.splitlines()
        if len(proxies) < 10:
            print("Error: Not enough proxies available.")
            return None
        random.shuffle(proxies)
        return proxies[:10]
    except Exception as e:
        print(f"Error while fetching proxies: {e}")
        return None

def print_and_save_proxies(proxies):
    if proxies:
        print(Colorate.Horizontal(Colors.green_to_white, "Tieni 10 sigma proxy:"))
        for idx, proxy in enumerate(proxies, start=1):
            print(f"{idx}. {proxy}")
        
        save_option = Write.Input("Do you want to save the proxy in a file? (yes/no): ", Colors.blue_to_white)
        if save_option.lower() == "yes":
            with open('sigmaproxy.txt', 'w') as f:
                f.write("\n".join(proxies))
            print(Colorate.Horizontal(Colors.green_to_white, "Proxy saved to 'sigmaproxy.txt'."))

    else:
        print("No proxy were retrieved.")

def proxygen():
    proxies = get_proxy()
    print_and_save_proxies(proxies)

def check_token(token, results):
    headers = {"Authorization": token}
    try:
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if res.status_code == 200:
            results.append((token, "Valid"))
        elif res.status_code == 403:
            results.append((token, "Locked"))
        elif res.status_code == 429:
            results.append((token, "Rate Limited"))
        else:
            results.append((token, "Invalid"))
    except Exception as e:
        results.append((token, f"Error: {e}"))

def token_checker():
    try:
        tokens = open('assets/tokens.txt', 'r').read().splitlines()
    except FileNotFoundError:
        print(Fore.LIGHTRED_EX + "Error: File 'assets/tokens.txt' not found. Please make sure it exists.")
        return

    if not tokens:
        print(Fore.LIGHTRED_EX + "No tokens found in the file.")
        return

    results = []
    threads = []

    for token in tokens:
        thread = threading.Thread(target=check_token, args=(token, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    for token, status in results:
        color = Colors.green_to_white if status == "Valid" else Colors.red_to_white
        print(Colorate.Horizontal(color, f"{status} : {token}", 1))

def spam_token(token, message, channel_id, num_spams, results):
    headers = {"Authorization": token}
    payload = {"content": message}
    for _ in range(num_spams):
        try:
            res = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)
            if res.status_code == 200:
                results.append((token, "Message Sent"))
            elif res.status_code == 403:
                results.append((token, "Forbidden"))
            elif res.status_code == 429:
                results.append((token, "Rate Limited"))
            else:
                results.append((token, f"Failed ({res.status_code})"))
        except Exception as e:
            results.append((token, f"Error: {e}"))

def token_spammer():
    try:
        tokens = open('assets/tokens.txt', 'r').read().splitlines()
    except FileNotFoundError:
        print(Fore.LIGHTRED_EX + "Error: File 'assets/tokens.txt' not found. Please make sure it exists.")
        return

    if not tokens:
        print(Fore.LIGHTRED_EX + "No tokens found in the file.")
        return

    channel_id = Write.Input("Enter the Channel ID to spam: ", Colors.blue_to_white)
    message = Write.Input("Enter the Message to spam: ", Colors.blue_to_white)
    num_spams = int(Write.Input("Enter the number of times to spam the message: ", Colors.blue_to_white))

    results = []
    threads = []

    for token in tokens:
        thread = threading.Thread(target=spam_token, args=(token, message, channel_id, num_spams, results))
        threads.append(thread)
        thread.start()
        time.sleep(0.2)

    for thread in threads:
        thread.join()

    for token, status in results:
        color = Colors.green_to_white if status == "Message Sent" else Colors.red_to_white
        print(Colorate.Horizontal(color, f"{status} : {token}", 1))

def spam_webhook(webhook_url, message, num_spams, results):
    payload = {"content": message}
    for _ in range(num_spams):
        try:
            res = requests.post(webhook_url, json=payload)
            if res.status_code == 204:
                results.append(("Webhook", "Message Sent"))
            elif res.status_code == 429:
                results.append(("Webhook", "Rate Limited"))
            else:
                results.append(("Webhook", f"Failed ({res.status_code})"))
        except Exception as e:
            results.append(("Webhook", f"Error: {e}"))

def webhook_spammer():
    webhook_url = Write.Input("Enter the Webhook URL: ", Colors.blue_to_white)
    message = Write.Input("Enter the Message to spam: ", Colors.blue_to_white)
    num_spams = int(Write.Input("Enter the number of times to spam the message: ", Colors.blue_to_white))

    results = []
    threads = []

    for _ in range(num_spams):
        thread = threading.Thread(target=spam_webhook, args=(webhook_url, message, 1, results))
        threads.append(thread)
        thread.start()
        time.sleep(0.2)

    for thread in threads:
        thread.join()

    for source, status in results:
        color = Colors.green_to_white if status == "Message Sent" else Colors.red_to_white
        print(Colorate.Horizontal(color, f"{status} : {source}", 1))

def botnuke():
    print("REVENANT BOT NUKE LINKS:")
    print("Brutto frocio aspetta che ancora li devo fare")

def ipinfo(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Error: {response.status_code} - boh non funziona."
    
    except Exception as e:
        return f"Errore nella richiesta bohh: {e}"

ip_address = input("Inserisci un indirizzo IP acer sigma: ")
info = ipinfo(ip_address)

if isinstance(info, dict):
    print("Info su IP sigma:")
    for key, value in info.items():
        print(f"{key}: {value}")
else:
    print(info)
input("")


def info():
    print(Fore.BLUE + "zGhiandaz isn't beautiful ha ha aha haxor")
    print(Fore.LIGHTCYAN_EX + "JOIN NOW")
    print(Fore.GREEN + "https://www.roblox.com/it/communities/11589616/Acorn-on-top#!/about")

if opt == 1:
    token_spammer()
elif opt == 2:
    token_checker()
elif opt == 3:
    webhook_spammer()
elif opt == 4:
    botnuke()
elif opt == 5:
    proxygen()
elif opt == 6:
    ipinfo()
elif opt == 7:
    info()
else:
    print(Fore.LIGHTRED_EX + "Coglioneeeeee, scegli tra 1, 2, 3, 4, 5 o 6.")

input(Fore.LIGHTRED_EX + "\nPress Enter to exit the program...")
