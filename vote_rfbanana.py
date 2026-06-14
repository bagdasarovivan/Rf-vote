from playwright.sync_api import sync_playwright
import random
import time

ACCOUNTS = [
    "benz123",
    "benz1231",
    "benz1232",
    "benz1233",
    "benz1234",
    "benz1235",
    "benz1236",
    "benz1237",
    "benz1238",
    "benz1239",
]

def vote(login):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://cp.rfbanana.ru/index.php?do=all_vote2026")
        page.wait_for_timeout(2000)

        # Вводим логин
        page.fill("input[type='text']", login)
        page.wait_for_timeout(500)
        
        # Нажимаем OK
        try:
            page.click("input[value='OK']")
        except:
            try:
                page.click("input[type='button']")
            except:
                page.keyboard.press("Enter")
        
        page.wait_for_timeout(3000)

        # Ищем кнопки Vote Now
        vote_buttons = page.query_selector_all("a, button, input[type='button']")
        clicked = 0
        for btn in vote_buttons:
            try:
                if not btn.is_visible():
                    continue
                text = btn.inner_text()
                if "Vote" in text:
                    btn.click()
                    print(f"[{login}] Нажата: {text}")
                    page.wait_for_timeout(2000)
                    clicked += 1
            except:
                continue

        if clicked == 0:
            print(f"[{login}] Кнопки неактивны")
        else:
            print(f"[{login}] Готово! Нажато: {clicked}")

        browser.close()

# Случайная задержка 0-10 минут перед стартом
delay = random.randint(0, 600)
print(f"Ждём {delay} секунд перед запуском...")
time.sleep(delay)

for account in ACCOUNTS:
    vote(account)
    # Небольшая пауза между аккаунтами
    time.sleep(random.randint(5, 15))
