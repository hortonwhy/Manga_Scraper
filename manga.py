from bs4 import BeautifulSoup
import requests
import os
import time
from urllib.request import Request, urlopen


#want to add an automatic zip function, maybe who knows.

global manga

class Manga:
    def __init__(self,urls, head_title, title):
        self.urls = urls
        self.main_title = head_title
        self.title = title


def main():
    url = 'https://manganelo.com/manga/garden_sphere'
    domain = 'manganelo.com'
    link_list = []

    site = 'https://manganelo.com/manga/garden_sphere'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)

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
        time.sleep(5)

        for div in page_soup.find_all('div', {'class': 'container-chapter-reader'}):
            time.sleep(2)
            img_list = (div.find_all('img'))
            for img in img_list:
                src_list.append(img.get('src'))
            manga = Manga(src_list, head_title, title)
            img_get_file(manga)


def img_get_file(manga):
    print(manga.title)
    time.sleep(2)
    counter = 0
    cwd_name = os.getcwd()
    manga_title = manga.title
    filename = cwd_name+'/'+ manga.main_title+'/'+'{}'.format(manga_title) +'/'
    try:
        os.makedirs(filename)
    except:
        print('Directory for {} already exists.'.format(filename))

    for link in manga.urls:
        time.sleep(5)
        img_dl = requests.get(link)
        if img_dl.status_code == 200:
            #ISSUE, some pages give 403 errors even when images are available
            #May be site side
                with open(filename+'/'+'{}.png'.format(counter), 'wb') as f:
                    f.write(img_dl.content)
                    counter += 1
                    print('counter:', counter)
        else:
            print('response was',img_dl.status_code)

main()
