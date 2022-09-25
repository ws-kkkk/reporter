from turtle import title
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from datetime import datetime

service = Service(executable_path=ChromeDriverManager().install())
url = "https://www.acfun.cn/login/?returnUrl=https%3A%2F%2Fwww.acfun.cn%2F"

def Login():
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("headless")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        print(driver.title)

        time.sleep(2)

        driver.find_element(By.XPATH, "//*[@id=\"login-account-switch\"]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id=\"ipt-account-login\"]").send_keys("17738285376")
        driver.find_element(By.XPATH, "//*[@id=\"ipt-pwd-login\"]").send_keys("nangua123.")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id=\"form-login\"]/div[4]/div").click()
        
        # title = str(driver.title)
        time.sleep(1)
        tips = driver.find_element(By.XPATH,"//*[@id=\"prompt-tips\"]")
        info = tips.get_attribute("innerHTML")
        if info == "帐号不存在或密码错误":
            print(info)
            driver.quit()
        else:
            print("登录成功")
        time.sleep(100)

    except Exception as e:
        print("异常，登录失败")
        print(str(e))

if __name__ == "__main__":
    Login()