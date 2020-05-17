import os, sys
import ctypes
import random

from bs4 import BeautifulSoup as BS
import requests


sectors = ['dark-colors-computer-wallpaper', 'dark-theme-wallpaper',
     'cool-dark-wallpapers', 'dark-desktop-wallpaper', 'dark-beautiful-wallpaper',
     'pretty-black-wallpaper', 'dark-pretty-wallpaper','dark-hd-wallpapers-1080p'
     'epic-space-wallpaper', 'epic-1080p-wallpapers', 'space-star-background',
     'deep-space-backgrounds']

url_frame = "https://wallpapersafari.com/{0}/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

home_path = os.path.expanduser('~')
wallpaper_path = '.wallpaper_files/wallpaper.{0}'
path = os.path.join(home_path, wallpaper_path)

try:
    random.shuffle(sectors)
except:
    file_path = path.format('png')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)
    sys.exit(1)

sector = random.choice(sectors)
url = url_frame.format(sector)
response = requests.get(url, headers=headers)
soup = BS(response.content, 'lxml')

links = []
for img_block in soup.find_all("img", class_="img-fluid"):
    link = img_block['src']
    links.append(link)

wallpaper = random.choice(links)
ext = wallpaper.split(".")[-1]
file_path = path.format(ext)
image_raw = requests.get(wallpaper, headers=headers)
with open(file_path, 'wb') as wr:
    wr.write(image_raw.content)
ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)

