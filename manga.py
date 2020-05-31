from bs4 import BeautifulSoup
import requests
import os
import time
import urllib.request
#from img_download import img_get

# I want to make a manga scraper that, given a url
# will download each chapter and compress and return an archive
# that has each chapter in hierarchal order, etc...
# i also want to implement this into a web app, so you go to this website
# and put the url in and within time, you receive a download for a zIp


#this is how you get the page info from a url
#domain = print(input('Enter the domain of the website, ex: manganelo.com: '))
global manga

class Manga:
    def __init__(self,urls, head_title, title):
        self.urls = urls
        self.main_title = head_title
        self.title = title


def main():
    url = 'https://manganelo.com/manga/garden_sphere'
    domain = 'manganelo.com'
    result = requests.get(url)
    print(result.status_code)
    link_list = []

    src = result.content    #stores page content to variable

    soup = BeautifulSoup(src, 'lxml') #parses and processes the source
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
                #print(img.get('src'))
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
                with open(filename+'/'+'{}.png'.format(counter), 'wb') as f:
                    f.write(img_dl.content)
                    counter += 1
                    print('counter:', counter)
