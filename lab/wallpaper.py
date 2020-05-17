from bs4 import BeautifulSoup as BS
import urllib.request
import requests
import ctypes
import random
#local modules
import config

#Defualt params Here
key1 = "dark"
key2 = "wallpaper"

url = "https://www.google.com/search?q={0}+{1}+{2}&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjZlrPcos3gAhWBs48KHTF6DEAQ_AUIDigB&biw=1366&bih=625"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def keywords(url):
    key_list = [
        "aesthetic", "1080p", "depression", "tumblr", "korean",
        "laptop", "nature", "fantasy", "4K","ultra hd", "gothic",
        "darkside", "popular", "retina"
     ]
    choice = random.choice(key_list)
    url = url.format(key1, key2, choice)
    return url

response = requests.get(keywords(url), headers=headers)
soup = BS(response.content, 'lxml')
print(soup.prettify())
links = []
#    for img_block in soup.find_all("img", class_="img-fluid"):
#        link = img_block['src']
#        links.append(link)

#    wallpaper = random.choice(links)
#    ext = wallpaper.split(".")[-1]
#    path = f"F:/programs/wallpaper/pictures/wallpaper.{ext}"
#    image_raw = requests.get(wallpaper, headers=headers)
#    with open(path, 'wb') as wr:
#        wr.write(image_raw.content)
#    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

#except:
#    path = "F:/programs/wallpaper/pictures/wallpaper.png"
#    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
