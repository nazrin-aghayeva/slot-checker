import requests
import os

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://lift-api.vfsglobal.com/appointment/CheckIsSlotAvailable"

payload = {
    "countryCode":"aze",
    "missionCode":"cze",
    "vacCode":"CBAK",
    "visaCategoryCode":"fam",
    "roleName":"Individual",
    "loginUser":"nazrinaghayeva@gmail.com",
    "payCode":""
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg}
    )

try:
    r = requests.post(URL, json=payload, headers=headers, timeout=30)

    if r.status_code != 200:
        print("Bad status:", r.status_code)
        print(r.text[:200])
        exit()

    try:
        data = r.json()
    except Exception:
        print("Not JSON response:")
        print(r.text[:500])
        exit()

    if data.get("earliestSlotLists"):
        send("🚨 SLOT AVAILABLE — BOOK NOW")
    else:
        print("No slots")

except Exception as e:
    print("Request failed:", e)
