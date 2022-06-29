
import sqlite3
from tkinter.filedialog import askopenfilename
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pymsgbox as pg
import sqlite3
from tkinter import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# # driverpth = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
# photopath = askopenfilename(filetypes=[("Select Images", ".png .jpg .jpeg")])
# phototext = "Testing the Image"


def UploadTOIG(Image, description, username):
    if len(username) != 1:
        for i in username:
            UploadToInstagram(Image, description, i)
    else:
        UploadToInstagram(Image, description, username[0])

def UploadToInstagram(Image, description, username):
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    userdetails = cursor.execute(f'select * from Instagram where username="{username}"').fetchall()
    username = userdetails[0][0]
    passwd = userdetails[0][1]
    driverpth = userdetails[0][2]
    # exit()
    option = webdriver.ChromeOptions()
    option.binary_location = driverpth
    option.add_argument("--incognito")
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    # option.add_argument("--headless")
    browser = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=option)
    browser.maximize_window()
    browser.get("https://instagram.com")
    time.sleep(10)
    browser.find_element(
        By.NAME, "username").send_keys(username)
    browser.find_element(
        By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input").send_keys(passwd)
    browser.find_element(
        By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]").click()
    time.sleep(5)
    browser.get(f'https://instagram.com/{username}')
    time.sleep(10)
    browser.find_element(
        By.CSS_SELECTOR, '[aria-label="New Post"]').click()


# To Stop until Loaded 

# username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, “input[name=’username’]”)))
# password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

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
    if username == None:
        exit()
    password = pg.prompt('Enter your Instagram Password', config[0])
    if password == None:
        exit()
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


def UpdateAndDeleteInstagram():
    TableName = "Instagram"
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    Apps = cursor.execute(f'select * from {TableName}').fetchall()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    tempPlace = 1
    tempPlacee = 0


    def InstagramUpdate(username):
        user = cursor.execute(
            f'select * from "{TableName}" where username="{username}"').fetchall()[0]
        newUsername = pg.prompt(
            f"Enter the New User ( If Changed )\n\nCurrent Username is {user[0]}", config[0], default=user[0])
        if newUsername == None:
            exit()
        newPassword = pg.prompt(
            f"Enter the New Password ( If Changed )\n\nCurrent Username is {user[1]}", config[0], default=user[1])
        if newPassword == None:
            exit()
        pg.alert("In the Next step we'll ask your browser Location Select the old one if you do not want to change the Browser")
        data = str(user[2]).split("/")[-1]
        data = str(user[2]).replace(f"/{data}", "")
        newBrowserLocation = askopenfilename(initialdir=data)
        if newUsername == user[0] and newPassword == user[1] and newBrowserLocation == user[2]:
            pg.alert("Nothing has been changed so nothing is changed in DataBase")
        else:
            cursor.execute(
                f'update "{TableName}" set "username"="{newUsername}", "password"="{newPassword}", "browserPath"="{newBrowserLocation}" where "username"="{user[0]}"')
            connection.commit()


    def InstagramDelete(username):
        cursor.execute(f'delete from "{TableName}" where username="{username}"')
        connection.commit()


    root = Tk()
    root.geometry("700x500")
    root.title("App Configuration")
    root.resizable(height=False, width=False)

    textLabel = Label(root, text=f"{TableName} Configuration")
    textLabel.config(font=(20))
    textLabel.place(x=250, y=20)

    canvas = Canvas(root, width=600, height=400)
    frame = Frame(canvas)
    scroll_y = Scrollbar(root, orient="vertical", command=canvas.yview)

    for AppData in Apps:
        AppLabel = Label(frame, text=AppData[0], height=5)
        AppLabel.grid(padx=(30, 0))
        Button(frame, width=10, command=lambda m=AppData[0]: InstagramUpdate(m),
            text="Update").grid(row=tempPlacee, column=1, padx=(90, 0))
        Button(frame, width=10, command=lambda m=AppData[0]: InstagramDelete(m),
            text="Delete").grid(row=tempPlacee, column=1, padx=(250, 0))

        tempPlacee += 1

    canvas.create_window(0, 0, anchor='nw', window=frame, width=600)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                    yscrollcommand=scroll_y.set)
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
    canvas.focus_set()
    canvas.place(x=50, y=50)

    root.mainloop()
