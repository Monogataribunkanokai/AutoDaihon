import requests
from typing import Union
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os
import re
from pprint import pprint
from rubi import AddRuby
from string import Template
class GetHTML():
    def __init__(self,url:str) -> None:
        self.__url=url
        self.__soup=self.__get_HTML_soup()
        self.__site_data=self.__get_HTML_data()
    def __get_HTML_data(self)->requests.models.Response:
        """Get HTML data from URL
        Returns:
            requests.models.Response: レスポンス
        """
        site_data=requests.get(self.__url)
        site_data.encoding=site_data.apparent_encoding
        return site_data
    def __get_HTML_soup(self):
        site_data=self.__get_HTML_data()
        soup=BeautifulSoup(site_data.text,'html.parser')
        return soup

    def download_HTML_row_file(self,save_path:str='',file_name:str|bool=False):
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
    def get_head(self):
        return self.__soup.find('head')
    def get_meta_body(self):
        return self.__soup.find('div',class_='metadata')
    def generate_ruby_HTML(self):
        main_text=self.get_main_text()
        main_text=re.sub(r'<ruby><rb>(.+?)<\/rb><rp>（<\/rp><rt>.*?<\/rt><rp>）</rp><\/ruby>','\\1',str(main_text))
        main_text=re.sub(r'<div class="main_text">','',str(main_text))
        main_text=main_text.replace('\n','')
        main_text=main_text.replace('<br/>','\n')
        main=main_text.split()
        #main=re.split(r'<br/>',main_text)
        add_ruby=AddRuby()
        result:str=''
        for t in main:
            result+=add_ruby.add_rubi(t)+'<br/>\n'
        main_text=result.rstrip('</div><br/>\n')
        main_text=Template('<div class="main_text"><br />$contents</div></body>').substitute(contents=main_text)
        main_text=str(self.get_head())+'<body>'+str(self.get_meta_body())+main_text
        return main_text
    def save_ruby_html(self):
        main_text=self.generate_ruby_HTML()
        with open (str(g.get_title())+'ルビ付き'+'.html','w') as f:
            f.write(main_text)

url:str='https://www.aozora.gr.jp/cards/000081/files/473_42318.html'
g=GetHTML(url=url)
g.save_ruby_html()