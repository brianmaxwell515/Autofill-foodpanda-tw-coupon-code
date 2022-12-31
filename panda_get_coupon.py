import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import time


def get_coupon_code():
    ua = UserAgent()
    r = requests.get("https://www.callingtaiwan.com.tw/foodpanda-coupon-code/", headers={
        "User-Agent": ua.random
    })
    coupon_code = set()
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.select('[data-code*=""]')
    for s in results:
        if "<span>" not in (s["data-code"]):
            coupon_code.add(s["data-code"])
    return coupon_code


def fill_coupon_code(coupon_code):
    # Please replace your firefox profile path {username} and {profile_folder}
    profile = webdriver.FirefoxProfile(
        'C:\\Users\\{username}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\{profile_folder}')

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.implicitly_wait(10)
    driver.get("https://www.foodpanda.com.tw/vouchers")

    for i in coupon_code:
        try:
            couponLink = driver.find_element(
                By.XPATH, "//button[@class='voucher-wallet__save-voucher cl-interaction-primary f-14 fw-normal']")
            couponLink.click()
            time.sleep(1)
        except ElementClickInterceptedException:
            print("Trying to click on the button again")

        couponCodeInput = driver.find_element(
            By.XPATH, "//input[@id='voucher-code']")
        couponCodeInput.clear()
        couponCodeInput.send_keys(i)
        couponCodeInput.send_keys(Keys.ENTER)
        time.sleep(1)
    driver.quit()


# get coupon code from website
coupon_code = get_coupon_code()

# fill in coupon code to foodpanda account
fill_coupon_code(coupon_code)
