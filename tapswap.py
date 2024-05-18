import requests
import json
import time
from colorama import init, Back, Fore, Style

# Initialize colorama
init(autoreset=True)

init_data = ""# can get in tapswap offline page

TAP = 50# tap almonts
TIME = 2# sleep time

def getToken(init_data):
    url = "https://api.tapswap.ai/api/account/login"
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "api.tapswap.ai",
        "Origin": "https://app.tapswap.club",
        "Referer": "https://app.tapswap.club/",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-App": "tapswap_server",
        "X-Cv": "bot_key",
    }
    data = {
        "bot_key": "app_bot_0",
        "init_data": init_data,
        "referrer": ""
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["access_token"]

def tap(token):
    url = "https://api.tapswap.ai/api/player/submit_taps"
    payload = {
        "taps": 50,
        "time": int(time.time())
    }

    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Content-Id": "51158",
        "Content-Type": "application/json",
        "Host": "api.tapswap.ai",
        "Origin": "https://app.tapswap.club",
        "Referer": "https://app.tapswap.club/",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-App": "tapswap_server",
        "X-Cv": "1"
    }

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return {"energy": response.json()["player"]["energy"], "asset": response.json()["player"]["shares"],"total":response.json()["player"]["asset"]["taps"]}
        except requests.exceptions.RequestException as e:
            if attempt + 1 == max_retries:
                raise
            time.sleep(TIME)  # Wait before retrying

while True:
    token = getToken(init_data)
    for i in range(51):
        try:
            data = tap(token)
            energy = data["energy"]
            asset = data["asset"]
            taps = data["total"]
            print(f"\t{Back.GREEN}{Fore.BLACK} Energy: {energy} {Style.RESET_ALL}\t{Back.BLUE}{Fore.WHITE} Asset: {asset} {Style.RESET_ALL}\n{Back.RED}{Fore.WHITE} Total Tap: {taps}{Style.RESET_ALL} ")

            time.sleep(TIME)
        except Exception as e:
            break