import requests
from bs4 import BeautifulSoup, Tag
import os
import re
from string import Template
from AddRuby import AddRuby


class GetHTML:
    def __init__(self, url: str) -> None:
        self.__url = url
        self.__soup = self.__get_HTML_soup()
        self.__site_data = self.__get_HTML_data()
        self.__generated_HTML: str = ""

    def __get_HTML_data(self) -> requests.models.Response:
        """Get HTML data from URL
        Returns:
            requests.models.Response: レスポンス
        """
        site_data = requests.get(self.__url)
        site_data.encoding = site_data.apparent_encoding
        return site_data

    def __get_HTML_soup(self) -> BeautifulSoup:
        site_data = self.__get_HTML_data()
        soup = BeautifulSoup(site_data.text, "html.parser", from_encoding="Shift_JIS")
        # print(soup)
        return soup

    def download_HTML_row_file(
        self, save_path: str = "", file_name: str | bool = False
    ) -> str:
        """URLからHTMLをダウンロードする

        Args:
            save_path (str, optional): ダウンロードしたファイルを保存するディレクトリパス. Defaults to ''.
            file_name (変更するファイル名 | bool, optional): ファイル名を変更するかどうか. Defaults to False.
        Returns:
            str : 保存したファイルパス
        """
        if isinstance(file_name, bool):
            if not file_name:
                save_path = os.path.join(save_path, str(self.__get_title()) + ".html")
            else:
                save_path = os.path.join(save_path, str(file_name))
        with open(save_path, mode="w") as file:
            file.write(self.__site_data.text)
        return save_path

    def __get_title(self) -> str | None:
        """文庫タイトルを取得する
        Returns:
            str: タイトル
        """
        titel_text: str | None = None
        blocks = self.__soup.find("meta", attrs={"name": "DC.Title"})
        if isinstance(blocks, Tag):
            content = blocks.get("content")
            if isinstance(content, str):
                titel_text = content
            elif isinstance(content, list):
                titel_text = content[0]
        return titel_text

    def __get_creator(self) -> str | None:
        """作者を取得する

        Returns:
            str : 作者
        """
        creator_text: str | None = None
        blocks = self.__soup.find("meta", attrs={"name": "DC.Creator"})
        if isinstance(blocks, Tag):
            content = blocks.get("content")
            if isinstance(content, str):
                creator_text = content
            elif isinstance(content, list):
                creator_text = content[0]
        return creator_text

    def __get_main_text(self):
        main_text = self.__soup.find("div", class_="main_text")
        return main_text

    def __get_head(self):
        return self.__soup.find("head")

    def __get_meta_body(self):
        return self.__soup.find("div", class_="metadata")

    def generate_ruby_HTML(self, line_number: int = 45):
        main_text = self.__get_main_text()
        # 本文のルビを削除
        main_text = re.sub(
            r"<ruby><rb>(.+?)<\/rb><rp>（<\/rp><rt>.*?<\/rt><rp>）</rp><\/ruby>",
            "\\1",
            str(main_text),
        )
        main_text = re.sub(r'<div class="main_text">', "", str(main_text))
        main_text = main_text.replace("\n", "")
        main_text = main_text.replace("<br/>", "\n")
        main: list[str] = []
        for u in main_text.split():
            if len(u) > line_number:
                main.append(u[:line_number] + "\n" + u[line_number:])
            else:
                main.append(u)
        # main=re.split(r'<br/>',main_text)
        add_ruby = AddRuby()
        result: str = ""
        for t in main:
            result += add_ruby.add_HTML_ruby(t) + "<br/>\n"
        main_text = result.rstrip("</div><br/>\n")
        main_text = Template(
            '<div class="main_text"><br />$contents</div></body>'
        ).substitute(contents=main_text)
        main_text = (
            str(self.__get_head()) + "<body>" + str(self.__get_meta_body()) + main_text
        )
        self.__generated_HTML = main_text
        return main_text

    def save_ruby_html(self):
        main_text = self.__generated_HTML
        with open(str(self.__get_title()) + "ルビ付き" + ".html", "w") as f:
            f.write(main_text)
