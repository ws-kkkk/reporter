from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json

service = Service(executable_path=ChromeDriverManager().install())
url = "https://ids.cqupt.edu.cn/authserver/login?service=http%3A%2F%2Fehall.cqupt.edu.cn%2Fpublicapp%2Fsys%2Fcyxsjkdkmobile%2F*default%2Findex.html"

with open("report_setting.json", 'r', encoding="utf-8") as f:
    default_str = f.read()
opt = json.loads(default_str)
username = opt["cqupt"]["username"]
password = opt["cqupt"]["password"]
mail_account = opt["mail"]["account"]
smtp_password = opt["mail"]["password"]
smtp_host = opt["mail"]["smtp_host"]


address_info = opt["address"]

def login_and_reporter():
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("headless")  #在linux无可视化界面下，不添加此参数会导致失败
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        print(driver.title)

        time.sleep(2)

        driver.find_element(By.XPATH, "//*[@id=\"username\"]").send_keys(username)
        driver.find_element(By.XPATH, "//*[@id=\"password\"]").send_keys(password)
        time.sleep(2)
        driver.find_element(By.XPATH, "//*[@id=\"login_submit\"]").click()

        time.sleep(2)
        print("正在修改表单....")
        title = str(driver.title)
        if title == "cyxsjkdkmobile":
            print("登录成功， 开始打卡")
        elif title in "重庆邮电大学统一身份认证平台" or title == "Unified Identity Authentication":
            msg = "学号或密码错误 或者 登录频繁，需要验证码"
            print(f"Error: {msg}")
            send_email(error=msg)
            driver.quit()
            return

        #=============== 这里处理一下重复打卡 =====================
        time.sleep(2)

        tips = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[2]/button/div/span").get_attribute("innerHTML")
        print(tips)

        if tips == "已打卡":
            print("今日已打卡，请勿重复打卡。")
        elif tips == "提交":
            write_info(driver)
            driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[2]/button").click() # 打卡提交
            time.sleep(1)
            after_tips = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[2]/button/div/span").get_attribute("innerHTML")
            if after_tips == "已打卡":
                print("提交成功，已打卡")
                send_email()
            
            else:
                print("提交异常，打卡失败")
                send_email(error="提交异常")
        driver.quit()
    except Exception as e:
        print("程序发生异常，打卡失败！！")
        print(str(e))
        send_email(error="程序运行异常")


def send_email(text="每日健康打卡", error=""):
    print("发送邮件")
    time_now = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    if len(error) == 0:
        content = f"{time_now}, 今日打卡成功!!"
    else:
        content = f"{time_now} {error}, 打卡失败!"
    # print(content)
    msg =MIMEText(content, 'plain', 'utf-8')
    msg["From"] = Header(mail_account, 'utf-8')
    msg["To"] = Header(mail_account, 'utf-8')
    subject = text
    msg["Subject"] = Header(subject, 'utf-8')
    try:
        server = smtplib.SMTP()
        server.connect(smtp_host, 25)
        server.login(mail_account, smtp_password)
        server.sendmail(mail_account, mail_account, msg.as_string())
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print("邮件发送失败！\n{}".format(e))

def write_info(driver):
    """
    这里是根据以往打卡历史默认选择，如需更改信息需要手动打卡更改历史
    """
    #目前居住地
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[1]/div[4]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[1]/div[6]/div/div[1]/button[2]").click()
    time.sleep(1)
    #详细居住地址
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[1]/div[7]/div[2]/div/textarea").send_keys(address_info)
    time.sleep(1)

    

if __name__ == "__main__":
    login_and_reporter()