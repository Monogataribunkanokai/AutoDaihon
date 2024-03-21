import json
from urllib import request
import xml.etree.ElementTree as ET
import regex #文字種判別
import codecs
from string import Template

class AddRuby():
    def __init__(self,grand:int=1) -> None:
        self.__APPID = "123"  # <-- ここにあなたのClient ID（アプリケーションID）を設定してください。
        self.__URL = "https://jlp.yahooapis.jp/FuriganaService/V2/furigana"
        self.__grand=grand
    def post(self,query:str):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Yahoo AppID: {}".format(self.__APPID),
            }
        param_dic = {
            "id": "1234-1",
            "jsonrpc": "2.0",
            "method": "jlp.furiganaservice.furigana",
            "params": {
            "q": query,
            "grade": self.__grand
            }
            }
        params = json.dumps(param_dic).encode()
        req = request.Request(self.__URL, params, headers)
        with request.urlopen(req) as res:
            body = res.read()
        return body.decode()
    def add_rubi(self,text:str):
        response = self.post(text)
        t=""
        p = regex.compile(r'\p{Script=Han}+') #漢字判定用正規表現らしい
        root= json.loads(response)
        result=root["result"]["word"]#ヘッダー切り離し
        for word in result:
            if 'furigana' in word: #ふりがなが入っていたら furiganaが含まれる
                if 'subword'in word: #カナ交じりだったらsubwordが含まれる
                    for kanamajiri in word["subword"]:
                        if p.fullmatch(kanamajiri["surface"]):
                            t+=Template('<ruby><rb>$surface</rb><rt>$furigana</rt></ruby>').substitute(surface=kanamajiri['surface'],furigana=kanamajiri['furigana'])
                        else:
                            t+=(kanamajiri["surface"])
                else:
                    t+=Template('<ruby><rb>$surface</rb><rt>$furigana</rt></ruby>').substitute(surface=word['surface'],furigana=word['furigana']) #漢字のみのフリガナ設定
            else:
                t+=str(word["surface"])
        return t