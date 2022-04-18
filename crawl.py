import requests 
import time 
import re
import os
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

def getdata(url): 
    r = requests.get(url) 
    return r.text 

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

# location need to change according to your chrome driver location
driver = webdriver.Chrome('/home/nind0932/Desktop/commerce/chromedriver_linux64/chromedriver')

driver.get('https://www.ferragamo.com/shop/us/en/women/shoes/valery-55-749544') 

time.sleep(6)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser') 

output = []

for item in soup.find_all('img', {"class": "product-gallery__image--r19"}):
    
    if item['src'] and item['src'][0:4] == 'http':
        output.append(item['src'])
    else:
        output.append(item['data-lazy'])

# if requires we can use the list
for i in range(len(output)):
    download(output[i],'download')


