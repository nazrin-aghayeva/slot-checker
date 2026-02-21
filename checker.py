from playwright.sync_api import sync_playwright
import os
import json

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
    import requests
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg}
    )

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://lift-api.vfsglobal.com")

    response = page.request.post(URL, data=json.dumps(payload))

    if response.status != 200:
        print("Blocked:", response.status)
        browser.close()
        exit()

    data = response.json()

    if data.get("earliestSlotLists"):
        send("🚨 SLOT AVAILABLE — BOOK NOW")
    else:
        print("No slots")

    browser.close()
