from playwright.sync_api import sync_playwright

ACCOUNTS = [
    "benz123",
    "benz1233",
]

def vote(login):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://cp.rfbanana.ru/index.php?do=all_vote2026")
        page.wait_for_timeout(2000)

        page.fill("input[type='text']", login)
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)

        buttons = page.query_selector_all("button, input[type='submit'], a")
        clicked = 0
        for btn in buttons:
            try:
                if not btn.is_visible():
                    continue
                text = btn.inner_text()
                if "Change" in text or "login" in text.lower() or text.strip() == "":
                    continue
                btn.click()
                print(f"[{login}] Нажата: {text}")
                page.wait_for_timeout(2000)
                clicked += 1
                if clicked >= 3:
                    break
            except:
                continue

        if clicked == 0:
            print(f"[{login}] Кнопки неактивны — таймер ещё не истёк")
        else:
            print(f"[{login}] Готово! Нажато: {clicked}")

        browser.close()

for account in ACCOUNTS:
    vote(account)
