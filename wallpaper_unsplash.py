import os, sys
import json
import ctypes
import random
from bs4 import BeautifulSoup as BS
import requests

url = "https://unsplash.com/search/photos/{0}"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def is_duplicate(link):
    home_path = os.path.expanduser('~')
    wallpaper_path = '.wallpaper_files/wallpaper.json'
    full_path = os.path.join(home_path, wallpaper_path)
    dir_path = os.path.dirname(full_path)
    duplicate = True

    if not os.path.exists(dir_path):
        print("generating config folder...")
        os.mkdir(dir_path)

    if not os.path.exists(full_path):
        print("Generating config file...")
        with open(full_path, 'w') as wf:
            links = {
                'wallpaper_urls': []
            }
            json.dump(links, wf, indent=2)
    else:
        print("Checking config file for duplicates....")
        with open(full_path, 'r') as wf:
            try:
                data = json.load(wf)
                urls = data.get('wallpaper_urls')
                if len(urls) >= 135:
                    urls = urls[20:]
                if not link in urls:
                    print("No duplicates found....")
                    urls.append(link)
                    duplicate = False
            except:
                print("Unknown error regenerating config file..")
                os.remove(full_path)
                is_duplicate(link)

        if not duplicate:
            print("Writing new entry to config....")
            with open(full_path, 'w') as wf:
                json.dump(data, wf, indent=2)

    return duplicate

def keywords(url):
    key_list = [
        "black", "shadow", "ghost", "night", "Neon",
        "space", "darkness", "dark", "Dark Background","Horror", "stars",
        "darkside", "universe", "moon", "galaxy"
     ]
    random.shuffle(key_list)
    choice = random.choice(key_list)
    url = url.format(choice)
    print("Url generated: ", url)
    return url

def random_wallpaper():
    try:
        response = requests.get(keywords(url), headers=headers)
    except:
        print("No connection: Exiting..")
        sys.exit(1)

    soup = BS(response.content, 'lxml')
    links = []
    print("Scanning for pictures...")
    for i in soup.find_all('img'):
        primary_img = i.get('src')

        if primary_img:
            contents = primary_img.split(".")
            small_images = primary_img.split("=")
            if not 'adserver' in contents and not 'crop&w' in small_images:
                links.append(primary_img)
    print("Got ", len(links), "images, Choosing random one.....")
    choice = random.choice(links)
    return choice

duplicate = True
while duplicate:
    wallpaper_url = random_wallpaper()
    duplicate = is_duplicate(wallpaper_url)

print("Downloading the images:", wallpaper_url)
image_raw = requests.get(wallpaper_url, headers=headers)
home_path = os.path.expanduser('~')
wallpaper_path = '.wallpaper_files/wallpaper.png'
path = os.path.join(home_path, wallpaper_path)

print("writing image to file...")
with open(path, 'wb') as wf:
    wf.write(image_raw.content)

print("changing the wallpaper")
ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
