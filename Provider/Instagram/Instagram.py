
import sqlite3
from tkinter.filedialog import askopenfilename
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pymsgbox as pg

username = "tirega3310"
# passwd = "6fM3eyEGXYm9hmS"
# driverpth = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
photopath = askopenfilename(filetypes=[("Select Images", ".png .jpg .jpeg")])
phototext = "Testing the Image"

def UploadToInstagram(Image, description, username):
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    userdetails = cursor.execute(f'select * from Instagram where username="{username}"').fetchall()
    username = userdetails[0]
    passwd = userdetails[1]
    driverpth = userdetails[2]
    exit()
    option = webdriver.ChromeOptions()
    option.binary_location = driverpth
    option.add_argument("--incognito")
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_argument("--headless")
    browser = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=option)
    browser.maximize_window()
    browser.get("https://instagram.com")
    time.sleep(10)
    browser.find_element(
        By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input").send_keys(username)
    browser.find_element(
        By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input").send_keys(passwd)
    browser.find_element(
        By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]").click()
    time.sleep(5)
    browser.get(f'https://instagram.com/{username}')
    time.sleep(5)
    browser.find_element(
        By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[3]/div").click()


    # ActionChains(browser).move_to_element(browser.find_element_by_xpath(
    #     "/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/button")).click().perform()
    # handle = f"[CLASS:#32770; TITLE:Open]"
    # autoit.win_wait(handle, 60)
    # autoit.control_set_text(handle, "ToolbarWindow32", photopath)
    # autoit.control_set_text(handle, "Edit1", photopath)
    # autoit.control_click(handle, "Button1")

    browser.find_element(
        By.XPATH, "/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/form/input").send_keys(Image)

    time.sleep(2)

    browser.find_element(
        By.XPATH, "/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button").click()

    time.sleep(2)

    browser.find_element(
        By.XPATH, "/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button").click()

    time.sleep(2)

    browser.find_element(
        By.XPATH, "/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea").send_keys(description)

    time.sleep(2)

    browser.find_element(
        By.XPATH, "/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button").click()

    time.sleep(2)
    ImageUploaded = False
    while ImageUploaded == False:
        try:
            myElem = browser.find_element(
                By.XPATH, "/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/img").click()
            ImageUploaded = True
        except:
            time.sleep(5)
            ImageUploaded = False
    time.sleep(5)

def InstallInstagram():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    username = pg.prompt('Enter your Instagram Username', config[0])
    password = pg.prompt('Enter your Instagram Password', config[0])
    browserPath = askopenfilename()
    if len(username) != 0 and len(password) != 0:
        cursor.execute('create table if not exists Instagram ( username Text, password Text, browserPath Text )')
        connection.commit()
        cursor.execute(f'insert into Instagram values ( "{username}", "{password}", "{browserPath}" )')
        cursor.execute(
            'update Apps set isInstalled = "Yes" where Platform = "Instagram"')
        connection.commit()
        return "Done"
    else:
        pg.alert('Creadentials not entered Properly\n\nNone of the things were saved.', config[0])
    connection.close()
    return ' Error'


def GuideInstagram():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    pg.alert('Enter your Username and Password when Prompted and then select your browser to open Instagram', config[0])
    connection.close()

# UploadToInstagram(photopath, "Test", username)