from playwright.sync_api import sync_playwright
import os, json, time, requests

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

API = "https://lift-api.vfsglobal.com/appointment/CheckIsSlotAvailable"
SITE = "https://visa.vfsglobal.com/aze/en/cze/login"

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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Open real site page so Cloudflare runs challenge
    page.goto(SITE, timeout=60000)

    # wait for challenge JS to finish
    time.sleep(8)

    # Now request API using same session cookies
    response = context.request.post(API, data=json.dumps(payload))

    print("status:", response.status)

    if response.status != 200:
        browser.close()
        exit()

    data = response.json()

    if data.get("earliestSlotLists"):
        send("🚨 SLOT AVAILABLE — BOOK NOW")
    else:
        print("No slots")

    browser.close()
