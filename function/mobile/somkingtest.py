# -*- coding: utf-8 -*-
import uiautomator2 as u2
from function.utils import Util
from function.base.base import Base
import os,time
import xml.etree.ElementTree as ET


AGILEAPP = "com.gionee.agileapp"
__author__ = 'suse'
device = "IZEAMF6LLJVSLNQC"
rootLogDir = Base.get_cur_dir(__file__)
currentLogDirName =time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
currentTimeStampLogDir = os.path.join(rootLogDir,currentLogDirName)
os.mkdir(currentTimeStampLogDir)
d = u2.connect_usb(device)
d.app_start(AGILEAPP)
d(scrollable=True).scroll.to(text="看了吗")
d(text="看了吗").sibling(resourceId="com.gionee.agileapp:id/launch").click()
d(packageName="com.gionee.agileapp",className="android.view.View").wait()
xml = d.dump_hierarchy()
# print(xml)
root = ET.fromstring(xml)
print(xml)
# nodes = root.findall(".//*[@package='com.gionee.agileapp']/node")
for node in root.findall(".//*[@package='com.gionee.agileapp']/node"):
    className = node.get("class")
    # childNode = node.find("..//*[@class='android.view.View']/node")
    if(className == "android.view.View"):
        d.app_start(AGILEAPP)
        d(scrollable=True).scroll.to(text="看了吗")
        d(text="看了吗").sibling(resourceId="com.gionee.agileapp:id/launch").click()
        time.sleep(3)
        bounds = node.get("bounds")
        bounds = bounds.replace("]",",").replace("[","")
        bounds = bounds[:-1]
        print(bounds)
        bound_list = bounds.split(",")
        x = int(bound_list[0])+(int(bound_list[2])-int(bound_list[0]))/2
        y = int(bound_list[1])+(int(bound_list[3])-int(bound_list[1]))/2
        d.click(x, y)
        print(str(x)+";"+str(y))
        time.sleep(8)
        currentStamp =time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
        d.screenshot(currentTimeStampLogDir+os.sep+currentStamp+".jpg")
        d.press("back")
        # print(str(x)+","+str(y))






# for elem in page.xpath('//ul[@class="zm-topic-cat-main"]/li'):
#         print elem.xpath('a/text()')[0]

# cmd = "adb -s %s shell monkey  -p com.gionee.agileapp -v -v --throttle 1000 --ignore-crashes --ignore-security-exceptions --ignore-timeouts 300 1>>%s 2>> %s" %(device, currentTimeStampLogDir + os.sep + "monkey.log", currentTimeStampLogDir + os.sep + "error.log")
# monkeyRs = Util.exccmd(cmd)


# d(text= "决战食神").click()
# if d(text='无法播放此视频。').exists and d(text='点击重试').exists:
#     print("suseusuuuuuuuuuuuuu")

# 检查是否白屏
# d.screenshot("11.png")
# d.dump_hierarchy()
# d.dump("hierarchy.xml")
# if d(text='决战食神').exists:
#     print("1111111111")






