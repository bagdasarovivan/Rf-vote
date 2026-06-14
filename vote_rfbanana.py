from playwright.sync_api import sync_playwright

ACCOUNTS = ["benz123"]  # добавьте другие логины если нужно

def vote(login):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://cp.rfbanana.ru/index.php?do=all_vote2026")
        page.wait_for_timeout(2000)
        page.fill("input[type='text']", login)
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)
        buttons = page.query_selector_all("button, input[type='submit']")
        clicked = 0
        for btn in buttons:
            text = btn.inner_text()
            if "Change" in text or "change" in text:
                continue
            btn.click()
            print(f"[{login}] Нажата: {text}")
            page.wait_for_timeout(2000)
            clicked += 1
            if clicked >= 3:
                break
        print(f"[{login}] Готово! Нажато: {clicked}")
        browser.close()

for account in ACCOUNTS:
    vote(account)
