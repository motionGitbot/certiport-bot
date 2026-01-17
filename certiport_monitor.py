import os
import time
import requests
from playwright.sync_api import sync_playwright

URL = "https://certiport.uz/uz/register"

EXAM = "IC3 Digital Literacy GS5"
LANG = "English"
MODULE = "Key Applications"
CITY = "Toshkent / Ташкент"

CHECK_EVERY_SECONDS = 10

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")


def tg_send(text):
    if not BOT_TOKEN or not CHAT_ID:
        print(text)
        return

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text}
    )


def check_calendar(page):
    yellow = page.locator("button:has-text(' ')")
    if yellow.count() > 0:
        tg_send("🟡 Certiport’da BO‘SH SANA paydo bo‘ldi!\n👉 https://certiport.uz/uz/register")
        return True
    return False


def main():
    tg_send("✅ Certiport bot ishga tushdi. Sana kuzatilyapti.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        while True:
            try:
                page.goto(URL, timeout=60000)
                time.sleep(5)

                if check_calendar(page):
                    time.sleep(300)

            except Exception as e:
                tg_send(f"⚠️ Xatolik: {e}")

            time.sleep(CHECK_EVERY_SECONDS)


if __name__ == "__main__":
    main()
