import os
import requests

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

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg}
    )

r = requests.post(URL, json=payload, timeout=20)
data = r.json()

if data.get("earliestSlotLists"):
    send("🚨 VISA SLOT AVAILABLE — BOOK NOW")
