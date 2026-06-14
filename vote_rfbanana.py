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

        # Вводим логин и нажимаем OK
        page.fill("input[type='text']", login)
        page.wait_for_timeout(500)
        page.click("button:has-text('OK')")
        page.wait_for_timeout(3000)

        # Ищем кнопки "Vote Now"
        vote_buttons = page.query_selector_all("button:has-text('Vote Now'), a:has-text('Vote Now'), input[value='Vote Now']")
        
        if not vote_buttons:
            print(f"[{login}] Кнопки неактивны — таймер ещё не истёк")
        else:
            for btn in vote_buttons:
                btn.click()
                print(f"[{login}] Нажата Vote Now")
                page.wait_for_timeout(2000)
            print(f"[{login}] Готово! Нажато: {len(vote_buttons)}")

        browser.close()

for account in ACCOUNTS:
    vote(account)
