from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

URL   = "https://cp.rfbanana.ru/index.php?do=all_vote2026"
LOGIN = "benz123"

def enter_login(driver, wait):
    login_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
    login_field.clear()
    login_field.send_keys(LOGIN)
    # Кнопка OK
    driver.find_element(By.XPATH, "//button[contains(text(), 'OK')] | //input[@value='OK']").click()
    time.sleep(2)
    print(f"Логин '{LOGIN}' введён.")

def find_vote_buttons(driver):
    buttons = driver.find_elements(By.XPATH, "//a | //button")
    return [b for b in buttons if b.text.strip().lower() == "vote"]

def run():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait   = WebDriverWait(driver, 15)

    try:
        print("Открываю сайт...")
        driver.get(URL)
        time.sleep(2)

        enter_login(driver, wait)

        vote_buttons = find_vote_buttons(driver)

        if not vote_buttons:
            print("Кнопки 'Vote' не найдены — таймер ещё не истёк.")
            print("Жду... (проверка каждые 60 сек)")

            while True:
                time.sleep(60)
                driver.refresh()
                time.sleep(2)
                try:
                    enter_login(driver, wait)
                except:
                    pass
                vote_buttons = find_vote_buttons(driver)
                if vote_buttons:
                    print(f"Кнопки появились! Найдено: {len(vote_buttons)}")
                    break

        print(f"Нажимаю {len(vote_buttons)} кнопок...")
        for btn in vote_buttons:
            print(f"  Клик: {btn.text.strip()}")
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)

        print("\nГотово! Все кнопки нажаты.")
        time.sleep(3)

    finally:
        driver.quit()
        print("Браузер закрыт.")

if __name__ == "__main__":
    run()
