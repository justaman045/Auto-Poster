from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

username = "tirega3310"
passwd = "6fM3eyEGXYm9hmS"
driverpth = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
photopath = "C:/Users/coder/Downloads/7oli08cl1wk81.png"
phototext = "Testing the Image"

option = webdriver.ChromeOptions()
option.binary_location = driverpth
option.add_argument("--incognito")
# option.add_experimental_option('excludeSwitches', ['enable-logging'])
# option.add_argument("--headless")
browser = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=option)
browser.maximize_window()
browser.get("https://instagram.com")
time.sleep(5)
browser.find_element(
    By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input").send_keys(username)
browser.find_element(
    By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input").send_keys(passwd)
browser.find_element(
    By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]").click()
time.sleep(20)
browser.find_element(
    By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/button")
browser.get(f'https://instagram.com/{username}')
time.sleep(5)
browser.find_element_by_xpath(
    '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[3]/div').click()


parent_h = browser.current_window_handle
# click on the link that opens a new window
handles = browser.window_handles  # before the pop-up window closes
handles.remove(parent_h)
browser.switch_to_window(handles.pop())
# do stuff in the popup
# popup window closes
browser.switch_to_window(parent_h)
# and you're back


time.sleep(220)
