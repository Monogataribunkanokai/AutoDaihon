import requests
from typing import Union
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os
class GetHTML():
    def __init__(self,url:str) -> None:
        self.__url=url
        self.__soup=self.__get_HTML_soup()
        self.__site_data=self.__get_HTML_data()
    def __get_HTML_data(self):
        site_data=requests.get(self.__url)
        site_data.encoding=site_data.apparent_encoding
        return site_data
    def __get_HTML_soup(self):
        site_data=self.__get_HTML_data()
        soup=BeautifulSoup(site_data.text,'html.parser')
        return soup
    def download_HTML_file(self,save_path:str='',file_name:str|bool=False):
        if type(file_name)==bool and file_name==False:
            save_path=os.path.join(save_path,str(self.get_title())+'.html')
        else:
            save_path=os.path.join(save_path,str(file_name))
        with open(save_path,mode='w') as file:
            file.write(self.__site_data.text)
    def get_title(self):
        titel_text=self.__soup.find('meta',attrs= {'name':'DC.Title'}).get('content')
        return titel_text
    def get_creator(self):
        titel_text=self.__soup.find('meta',attrs= {'name':'DC.Creator'}).get('content')
        return titel_text
    def get_main_text(self):
        main_text=self.__soup.find('div',class_='main_text')
        return main_text
url:str='https://www.aozora.gr.jp/cards/000081/files/473_42318.html'
g=GetHTML(url=url)
print(g.get_main_text())