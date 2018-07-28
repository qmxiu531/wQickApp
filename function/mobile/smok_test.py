# -*- coding: utf-8 -*-
from function.mobile.phone import Device
from function.utils import Util
import xml.etree.ElementTree as ET
import uiautomator2 as u2
from function.base.base import Base
import time,os,re
import subprocess
from function.mobile.mobile_traffic import Traffic
from function.screenshot.mobile_screenshot import Screenshot
from function.page.config import Config

ANDROID_VIEW_VIEW = "android.view.View"
ANDROID_VIEW_BUTTON = "android.widget.Button"
__author__ = 'suse'
AGILEAPP = "com.gionee.agileapp"
logger = Util.logger



class SmokingTest:
    def __init__(self,serial,app_pkg_name,app_name,screenshot_dir):
        self.serial = serial
        self.app_pkg_name = app_pkg_name
        self.d = u2.connect_usb(self.serial)
        self.d.watcher("DESKTOP_ICON_CREATE").when(text="创建快应用桌面图标").click(text="取消", className="android.widget.Button")
        self.d.watcher("PERMISSION").when(text="允许").click(text="允许")
        self.d.watcher("COMMAN_PERMISSION").when(text="始终同意").click(text="始终同意")
        self.d.watcher("CONFIRM_POP").when(text="确定").click(text="确定")
        self.d.watcher("PERMISSION_CONTINUE").when(text="继续").click(text="继续")
        self.d.watchers.run()
        self.app_name = app_name
        self.xml = ""
        self.currentTimeStampLogDir = screenshot_dir+os.sep+"mobile"
        if not os.path.exists(self.currentTimeStampLogDir):
            os.mkdir(self.currentTimeStampLogDir)


    # def init_screenshot_dir(self):
    #     rootLogDir = Base.get_cur_dir(__file__)
    #     currentLogDirName =time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    #     self.currentTimeStampLogDir = os.path.join(rootLogDir,currentLogDirName)
    #     os.mkdir(self.currentTimeStampLogDir)


    def launch_app(self):
        try:
            self.d.screen_on()
            self.d.unlock()
            # self.d.app_start(AGILEAPP)
            # self.d(scrollable=True).scroll.to(text=self.app_name)
            # self.d(text=self.app_name).sibling(resourceId=AGILEAPP+":id/launch").click()
            cmd = "adb -s "+self.serial+" shell am start -a com.gionee.agileapp.action.LAUNCH -e EXTRA_APP "+self.app_name
            logger.info(cmd)
            cmd_str = Util.exccmd(cmd)
            logger.info(cmd_str)
            time.sleep(5)
            self.d(packageName=AGILEAPP,className=ANDROID_VIEW_VIEW).wait()
            logger.info("启动'"+self.app_name+"'成功")
        except:
            logger.error(Base.printErr("启动'"+self.app_name+"'失败！！！"))
        currentStamp =time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
        self.d.screenshot(self.currentTimeStampLogDir+os.sep+currentStamp+".jpg")

    def get_hierarchy_xml(self):
        self.xml=self.d.dump_hierarchy()

    def do_test(self):
        root = ET.fromstring(self.xml)
        if self.d(text="应用已下架").exists:
            logger.info(self.app_name+" 应用已下架")
            self.d.press("back")
            cmd = "adb -s "+self.serial+" shell am force-stop "+AGILEAPP
            cmd_str =Util.exccmd(cmd)
            logger.info(cmd_str)
            return Config.NOT_NEED_TEST_CODE

        for node in root.findall(".//*[@package='"+AGILEAPP+"']/node"):
            class_name = node.get("class")
            if class_name == ANDROID_VIEW_VIEW or class_name ==  ANDROID_VIEW_BUTTON:
                self.launch_app()
                bounds = node.get("bounds")
                bounds = bounds.replace("]",",").replace("[","")
                bounds = bounds[:-1]
                # print(bounds)
                bound_list = bounds.split(",")
                x = int(bound_list[0])+(int(bound_list[2])-int(bound_list[0]))/2
                y = int(bound_list[1])+(int(bound_list[3])-int(bound_list[1]))/2
                self.d.click(x, y)
                logger.info(print(str(x)+";"+str(y)))
                time.sleep(15)
                currentStamp =time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
                self.d.screenshot(self.currentTimeStampLogDir+os.sep+currentStamp+".jpg")
                self.d.press("back")
        return Config.TEST_PASS_CODE
    def get_uid(self):
        #获取进程ID
        getProcessIdcmd = 'adb -s '+self.serial+' shell ps | grep '+self.app_pkg_name+'$'
        p = subprocess.Popen(getProcessIdcmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        content = p.stdout.readlines()
        if len(content) == 1:
            processId = content[0].split()[1]
        else:
            logger.error("not get processID")
        #获取进程对应的UID
        getUidcmd = 'adb -s '+self.serial+' shell cat /proc/' + str(int(processId)) + '/status | grep Uid'
        p = subprocess.Popen(getUidcmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        content = p.stdout.readlines()
        uidStr = str(content[0], encoding='utf-8')
        uidList = uidStr.strip().split('\t')
        print(uidList)
        uid = uidList[1]
        return uid



def main(serial=None,pkg_name=None,screenshot_dir=None):
    st = SmokingTest(serial,AGILEAPP,pkg_name,screenshot_dir)
    # st.init_screenshot_dir()
    st.launch_app()
    uid = st.get_uid()
    traffic = Traffic(serial,uid)
    before_traffic = traffic.get_app_traffic()  #运行之前流量
    st.get_hierarchy_xml()
    test_rs_code = st.do_test()
    if test_rs_code == Config.NOT_NEED_TEST_CODE:
        return Config.NOT_NEED_TEST_CODE

    after_traffic = traffic.get_app_traffic() #运行之后流量
    diff_traffic = after_traffic - before_traffic

    logger.info("diff_traffic="+str(diff_traffic))
    screenshot_obj = Screenshot(st.currentTimeStampLogDir)
    screenshot_obj.parse_screenshot()

    # 生成测试结果
    logger.info("***************************"+pkg_name+" 测试结果*************************")
    screenshot_dict = {"white_screenshot":"出现白屏","black_screenshot":"出现黑屏","screenshot_video_not_play":"视频无法播放","screenshot_error_dir":"快应用内部出现错误"}
    screenshot_child_dir=Util.listChildDir(st.currentTimeStampLogDir)
    if diff_traffic>0 and len(screenshot_child_dir) == 0:
        logger.info("测试结论:通过")
        return Config.TEST_PASS_CODE
    else:
        logger.info("测试结论:不通过")
        if diff_traffic <= 0:
            logger.info("不通过原因:无法连接网络，详情见截图")
        if len(screenshot_child_dir) >0:
             for (key,value) in screenshot_dict.items():
                if screenshot_child_dir.__contains__(key):
                    logger.info("不通过原因:"+value+"(见"+key+"文件夹截图)")
        return Config.TEST_FAILE_CODE

if __name__ == '__main__':
    main()





