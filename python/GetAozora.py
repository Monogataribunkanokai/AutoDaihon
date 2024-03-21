import requests
from typing import Union
from html.parser import HTMLParser

def get_HTML(url:str='https://www.aozora.gr.jp/cards/000081/files/473_42318.html',file_name:str|bool=False):
    site_data=requests.get(url)
    site_data.encoding=site_data.apparent_encoding
    with open('test.html','w',encoding='utf-8') as f:
        f.write(site_data.text)