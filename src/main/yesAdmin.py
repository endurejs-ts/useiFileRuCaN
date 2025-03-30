from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import os
from dotenv import load_dotenv
import urllib.parse
import json
load_dotenv()

ID = os.getenv("ID")
PWD = os.getenv("PWD")

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.kakamuka.com")
sleep(1)

main = WebDriverWait(driver, 10)
main.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="JS_topMenu"]/li[1]/a[1]')))
login_button = driver.find_element(By.XPATH, '//*[@id="JS_topMenu"]/li[1]/a[1]')
login_button.click()
sleep(2)

main.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]')))

input1 = driver.find_element(By.XPATH, '//*[@id="member_id"]')
input1.send_keys(ID)
sleep(1.3)

input2 = driver.find_element(By.XPATH, '//*[@id="member_passwd"]')
input2.send_keys(PWD)
sleep(2)

login_button_form = driver.find_element(By.XPATH, '//form[starts-with(@id, "member_form_")]/div/div/fieldset/a')
login_button_form.click()

sleep(3)

for i in range(27, 30):
    with open(f"../../dist/href{i}.json", "r", encoding="utf-8") as f:
        content = json.load(f)

    result_d = []
    for ctt in content:
        driver.get(ctt)
        main.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]')))
        sleep(1)

        cotBox = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[2]/div[3]')
        title = cotBox.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[2]/div[3]/div[2]/h2')
        category_code = driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/ol')
        price = cotBox.find_element(By.XPATH, '//*[@id="span_product_price_text"]')
        amount_per_box = cotBox.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[2]/div[3]/div[2]/div[3]/div[1]/table/tbody/tr[4]/td/span')
        expire_date = cotBox.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[2]/div[3]/div[2]/div[3]/div[1]/table/tbody/tr[5]/td/span')
        formatted_text = " > ".join(category_code.text.split("\n"))
        result_d.append({
            "link": ctt,
            "title": title.text,
            "location": formatted_text,
            "price": price.text,
            "amount_per_box": amount_per_box.text,
            "expire_date": expire_date.text
        })

        with open(f"../../finished/data{i}.json", "w", encoding="utf-8") as f:
            json.dump(result_d, f, ensure_ascii=False, indent=4)

driver.quit()