# -*- coding: utf-8 -*-
from function.utils import Util
import os
import cv2
import shutil
from function.baidu_ai.text_parse import TextAi
from function.utils import Util
__author__ = 'suse'
logger = Util.logger

class Screenshot:
    def __init__(self,screenshot_dir):
        self.screenshot_dir = screenshot_dir
        pass
    # 字节bytes转化kb\m\g
    def formatSize(self,bytes):
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            print("传入的字节格式不对")
            return "Error"

        return kb

        # if kb >= 1024:
        #     M = kb / 1024
        #     if M >= 1024:
        #         G = M / 1024
        #         return "%fG" % (G)
        #     else:
        #         return "%fM" % (M)
        # else:
        #     return "%fkb" % (kb)


    def parse_screenshot(self):
        jpgFiles=Util.filterFiles(self.screenshot_dir,['.jpg'])
        for jpg in jpgFiles:
            # print(jpg)
            jpg_path = os.path.join(self.screenshot_dir,jpg)
            logger.info(jpg_path)
            size = os.path.getsize(jpg_path)
            # print(self.formatSize(size))
            kb = self.formatSize(size)
            if kb<100:
                print(kb)
                is_white = self.is_white_img(jpg_path)
                logger.info("是否白屏:"+str(is_white))
                if is_white:
                    screenshot_white_dir = os.path.join(self.screenshot_dir,"white_screenshot")
                    if not os.path.exists(screenshot_white_dir):
                        os.makedirs(screenshot_white_dir)
                    shutil.copyfile(jpg_path,os.path.join(screenshot_white_dir,jpg))
                is_black = self.is_black_img(jpg_path)
                logger.info("是否黑屏:"+str(is_black))
                if is_black:
                    screenshot_black_dir = os.path.join(self.screenshot_dir,"black_screenshot")
                    if not os.path.exists(screenshot_black_dir):
                        os.makedirs(screenshot_black_dir)
                    shutil.copyfile(jpg_path,os.path.join(screenshot_black_dir,jpg))
            else:
                 baidu_ai = TextAi(jpg_path)
                 img_txt =str(baidu_ai.get_text())
                 if img_txt.find("无法播放") !=-1 or img_txt.find("重试") !=-1:
                     screenshot_video_not_play_dir = os.path.join(self.screenshot_dir,"screenshot_video_not_play")
                     if not os.path.exists(screenshot_video_not_play_dir):
                        os.makedirs(screenshot_video_not_play_dir)
                     shutil.copyfile(jpg_path,os.path.join(screenshot_video_not_play_dir,jpg))
                 if img_txt.find("很抱歉") !=-1 or img_txt.find("出现错误") !=-1:
                     screenshot_error_dir = os.path.join(self.screenshot_dir,"screenshot_error_dir")
                     if not os.path.exists(screenshot_error_dir):
                        os.makedirs(screenshot_error_dir)
                     shutil.copyfile(jpg_path,os.path.join(screenshot_error_dir,jpg))




    def is_white_img(self,img_path=None):
        img = cv2.imread(img_path)
        h, w = img.shape[:2]

        # 屏幕的1/4处是否全部为白色
        h_c_4 = int(h/4)
        w_c_4 = w
        for y in range(0, w_c_4):
            for x in range(h_c_4, h_c_4*2):
              # img[x, y] = 255
              if img[x, y][0] < 255 or img[x, y][1] < 255 or img[x, y][2] < 255:
                  return False
        # 屏幕的中间是否为白色
        h_c_2 = int(h/2)
        w_c_2 = w
        for y in range(0, w_c_2):
            for x in range(h_c_2-200, h_c_2+200):
              # img[x, y] = 255
              if img[x, y][0] < 255 or img[x, y][1] < 255 or img[x, y][2] < 255:
                  return False
        return True

    def is_black_img(self,img_path=None):
        img = cv2.imread(img_path)
        h, w = img.shape[:2]
        # 屏幕的1/4处是否全部为黑色
        h_c_4 = int(h/4)
        w_c_4 = w
        for y in range(0, w_c_4):
            for x in range(h_c_4, h_c_4*2):
              # img[x, y] = 255
              if img[x, y][0] >> 2 or img[x, y][1] > 2 or img[x, y][2] > 2:
                  return False
         # 屏幕的1/2处是否全部为黑色
        h_c_2 = int(h/2)
        w_c_2 = w
        for y in range(0, w_c_2):
            for x in range(h_c_2-200, h_c_2+200):
              # img[x, y] = 255
              if img[x, y][0] >> 2 or img[x, y][1] > 2 or img[x, y][2] > 2:
                  return False
        return True







if __name__ == '__main__':
    screenshot_obj = Screenshot("E:\\python_study\\wQickApp\\function\\mobile\\2018-07-18-15_59_23")
    screenshot_obj.parse_screenshot()





