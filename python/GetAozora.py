import requests
from typing import Union
from html.parser import HTMLParser
from bs4 import BeautifulSoup

def get_HTML_soup(url:str='https://www.aozora.gr.jp/cards/000081/files/473_42318.html',file_name:str|bool=False):
    site_data=requests.get(url)
    site_data.encoding=site_data.apparent_encoding
    soup=BeautifulSoup(site_data.text,'html.parser')
    return soup
class AnalyzeHTML():
    def __init__(self,soup) -> None:
        self.__soup=soup
    def get_title(self):
        titel_text=self.__soup.find('meta',attrs= {'name':'DC.Title'}).get('content')
        return titel_text
    def get_creator(self):
        titel_text=self.__soup.find('meta',attrs= {'name':'DC.Creator'}).get('content')
        return titel_text
soup=get_HTML_soup()
html_text=AnalyzeHTML(soup=soup)
print(html_text.get_creator())