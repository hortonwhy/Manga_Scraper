from bs4 import BeautifulSoup
import requests
import os
import time
import urllib.request
from urllib.request import Request, urlopen
import random
import re
#want to add an automatic zip function, maybe who knows.

global manga

class Manga:
    def __init__(self,urls, head_title, title):
        self.urls = urls
        self.main_title = head_title
        self.title = title


def main():
    domain = 'manganelo.com'
    link_list = []

    site = input("Enter manga's main url page: ")

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')

    head_title = soup.title.get_text()
    print(head_title)

    for link in soup.find_all('a', {'class': 'chapter-name text-nowrap'}):
        link_list.append(link.attrs['href'])

    for link in link_list:
        src_list = []
        chapter_page = requests.get(link)
        page_src = chapter_page.content
        page_soup = BeautifulSoup(page_src, 'lxml')
        title = page_soup.title.get_text()
        time.sleep(random.randint(3,5))

        for div in page_soup.find_all('div', {'class': 'container-chapter-reader'}):
            img_list = (div.find_all('img'))
            for img in img_list:
                src_list.append(img.get('src'))
            manga = Manga(src_list, head_title, title)
            if src_list == []:
                break
            else:
                img_get_file(manga)

def img_get_file(manga):
    print(manga.title)
    time.sleep(random.randint(4,6))
    counter = 1
    cwd_name = os.getcwd()
    manga_title = manga.title
    filename = cwd_name+'/'+ manga.main_title+'/'+'{}'.format(manga_title) +'/'
    try:
        os.makedirs(filename)
    except:
        print('Directory for {} already exists.'.format(filename))
# if s3 is in the link it needs to be switched!!!
# in the link s3.mkklcdnv3.com needs to be switched to s8.mkkldcdnv8.com
    for link in manga.urls:
        if re.findall('s..mkklcdnv.', link)[0] in link:
            #link = link.replace('s3.mkklcdnv3', 's8.mkklcdnv8')
            link = link.replace(re.findall('s..mkklcdnv.', link)[0], 's8.mkklcdnv8')
        img_dl = requests.get(link)
        time.sleep(random.randint(1,3))
        if img_dl.status_code == 200:
            #ISSUE, some pages give 403 errors even when images are available
            #May be site side
                with open(filename+'/'+'{}'.format(counter), 'wb') as f:
                    f.write(img_dl.content)
                    print('counter:', counter)
                    counter += 1
                    time.sleep(random.randint(1,2))
        else:
            print('response was',img_dl.status_code)

main()
