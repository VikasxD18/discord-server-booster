import requests, threading, os

os.system("cls" if os.name == "nt" else "clear")
tkn = "MTA1MzI1ODA4NTM5NDgwODg0Mg.GYFN6b.Vqtr3EvIki-7qbtb0glQvyIIPaVuI1np8z6nDI"
secret = "p32R8kNZQMjzIwpDGEnTtXiN6XY4SgN6"
client_id = "1053258085394808842"
redirect = "http://localhost:8080"
API_ENDPOINT = 'https://canary.discord.com/api/v9'
auth = "https://canary.discord.com/api/oauth2/authorize?client_id=1053258085394808842&redirect_uri=http%3A%2F%2Flocalhost%3A8080&response_type=code&scope=identify%20guilds.join"
guild = input("Guild ID: ")

def exchange_code(code):
  data = {
    'client_id': client_id,
    'client_secret': secret,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect
  }
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  r = requests.post(str(API_ENDPOINT) + '/oauth2/token', data=data, headers=headers)
#   print(r.status_code)
  if r.status_code in (200, 201, 204):
    return r.json()
  else:
    return False

def add_to_guild(access_token, userID):
  url = f"{API_ENDPOINT}/guilds/{guild}/members/{userID}"

  botToken = tkn
  data = {
    "access_token": access_token,
  }
  headers = {
    "Authorization": f"Bot {botToken}",
    'Content-Type': 'application/json'
  }
  r = requests.put(url=url, headers=headers, json=data)
#   print(r.status_code)
  return r.status_code

def get_headers(tk):
    headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US",
                "authorization": tk,
                "referer": "https://discord.com/channels/@me",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9007 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDA3Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTYxODQyLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    return headers

def get_user(access: str):
  endp = "https://canary.discord.com/api/v9/users/@me"
  r = requests.get(endp, headers={"Authorization": f"Bearer {access}"})
  rjson = r.json()
  return rjson['id']

def main(tk):
    headers = get_headers(tk)
    r = requests.post(auth, headers=headers, json={"authorize": "true"})
    # print(r.status_code)
    if r.status_code in (200, 201, 204):
        # print(r.json())
        location = r.json()['location']
        # print(location)
        code = location.replace("http://localhost:8080?code=", "")
        # print(code)
        exchange = exchange_code(code)
        print("[+] Authorized Token")
        access_token = exchange['access_token']
        userid = get_user(access_token)
        add_to_guild(access_token, userid)
        print("[+] Added to Guild %s" % (guild))
        r = requests.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)
        idk = r.json()
        # print(idk)
        for x in idk:
            id_ = x['id']
            # print(id_)
            payload = {"user_premium_guild_subscription_slot_ids": [id_]}
            r = requests.put(f"https://discord.com/api/v9/guilds/{guild}/premium/subscriptions", headers=headers, json=payload)
            if r.status_code in (200, 201, 204):
                print("[+] Boosted %s" % (guild))
            # print(r.json())

f = open("boost-tokens.txt", "r").readlines()
for tk in f:
    tk = tk.strip()
    threading.Thread(target=main, args=(tk,)).start()

