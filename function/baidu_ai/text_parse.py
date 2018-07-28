# -*- coding: utf-8 -*-
import urllib3,base64
from urllib.parse import urlencode
from aip import AipOcr


__author__ = 'suse'
ACCESS_TOKEN = '24.c06a31b78d57ba3a4129c6e7a5713adc.2592000.1534390002.282335-11545175'
APP_ID = '11545175'
API_KEY = 'lxaASPMHiOi5NPE8a0rnYXGU'
SECRET_KEY = 'eIFGnTbh1aU1RmVVjSzB5tSbjMQQuA15'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
urllib3.disable_warnings()
class TextAi:
    def __init__(self,img_path):
        self.img_path = img_path
        pass
    def get_file_content(self):
        with open(self.img_path, 'rb') as fp:
            return fp.read()
    def get_text(self):
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        image = self.get_file_content()
        result = client.basicGeneral(image)
        print(result)
        return result


if __name__ == '__main__':
     baidu_ai = TextAi("E:\\python_study\\wQickApp\\function\\mobile\\2018-07-19-13_56_52\\2018-07-19-13_58_24.jpg")
     baidu_ai.get_text()


