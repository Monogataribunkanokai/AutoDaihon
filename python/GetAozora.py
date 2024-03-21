import requests
from typing import Union
from html.parser import HTMLParser
from bs4 import BeautifulSoup

def get_HTML(url:str='https://www.aozora.gr.jp/cards/000081/files/473_42318.html',file_name:str|bool=False):
    site_data=requests.get(url)
    site_data.encoding=site_data.apparent_encoding
    soup=BeautifulSoup(site_data.text,'html.parser')
    titel_text=soup.find('meta',attrs= {'name':'DC.Title'}).get('content')
    print(titel_text)
    with open('test.html','w',encoding='utf-8') as f:
        f.write(site_data.text)
get_HTML()