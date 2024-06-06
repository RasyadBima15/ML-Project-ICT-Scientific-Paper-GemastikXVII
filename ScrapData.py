from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

browser_options = Options()
browser_options.add_argument('-- no sandbox')

browser_options.add_argument('disable-notification')
browser_options.add_argument('--disable-infobars')
browser_options.add_argument('--start-maximized')

service = Service(executable_path="msedgedriver.exe")

driver = webdriver.Edge(service=service)
driver.get("https://www.tiktok.com")

search = "jokowi"

time.sleep(5)  

#usahakan cepat login ke akun guest
i = 0
while i < 1 :
    try :
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/form/input")))
        element.send_keys(search)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        i = 1
    except :
        print('ada kesalahaan saat di pencarian')
        i = 1

time.sleep(5)  

ii = 0
while ii < 1 :
    try :
        print("ini di post")
        video = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]")))
        video.click()
        time.sleep(2)

        elementPost = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div[1]")))
        elementPost.click()
        time.sleep(2)
        ii = 1
    except :
        print('ada kesalahaan saat di post')
        ii = 1

time.sleep(2) 

#scroll comment
elementComment = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]")
for i in range(7000) :
    print("lagi scrolling")
    driver.execute_script("arguments[0].scrollIntoView();", elementComment)
    

# Ambil HTML dari halaman setelah melakukan scroll
html = driver.page_source

# Parsing HTML menggunakan BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Lakukan scraping data komentar di sini menggunakan BeautifulSoup
# Misalnya, temukan semua elemen komentar dan cetak teksnya

username = []
comment_list = []

for user in soup.find_all('a', class_="e1g2efjf4 css-fx1avz-StyledLink-StyledUserLinkName er1vbsz0") : 
    username.append(user.text)

# Mengambil semua elemen komentar
comments = soup.find_all('p', class_='css-xm2h10-PCommentText e1g2efjf6')

for comment in comments:
    comment_list.append(comment.text.strip())

# print(username)
# print(len(username))

listCols = ['Username', 'Comment']
dict_data = dict(zip(
    listCols, (username, comment_list)
))

# print(dict_data)

# with open('dataTiktok.json', 'w') as fp:
#     json.dump(dict_data, fp)

df = pd.read_csv("ScrapeDataFromTiktok.csv")
df_new = pd.DataFrame(data=dict_data)
# df.head()

df_concatenated = pd.concat([df, df_new], ignore_index=True)
df_concatenated.to_csv("ScrapeDataFromTiktok.csv", index=False, mode='a', header=False)

print()
print()

print("finish")

# print(comment_list)
# print(len(comment_list))

time.sleep(30)  

driver.quit()