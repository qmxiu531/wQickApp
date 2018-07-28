# coding=utf-8
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from function.base.base import Base
from function.base.base_page import BasePage
from time import sleep
from PIL import Image, ImageEnhance, ImageFilter
import os
from pytesseract import *
import cv2
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import requests, time
from function.utils import Util
from function.mobile import smok_test
from function.page.config import Config
from function.mobile.mobile_crash import dump_crash_info
from selenium.webdriver.support.wait import WebDriverWait

logger = Util.logger


# 封装然之登录页面功能类
class RanzhiLogin(BasePage):
    def __init__(self, web_screenshot_dir):
        BasePage.__init__(self)
        self.web_screenshot_dir = web_screenshot_dir
        self.app_download_dir = self.web_screenshot_dir+os.sep+"app_download_dir"
        if not os.path.exists(self.app_download_dir):
            os.mkdir(self.app_download_dir)

    # 然之页面的登录操作
    # self.url:然之的网址
    # username：登录然之的用户名
    # password：登录然之的密码
    def log_in(self, username, password):
        if self.open_from_excel() == False:  # 根据excel中的url打开浏览器
            return None
        sleep(2)  # 等待1秒（可选）
        try:
            self.driver.find_element_by_name("account").send_keys(username)  # 定位到用户名字段并输入用户名
            self.driver.find_element_by_name("password").send_keys(password)  # 定位到密码字段并输入密码
            self.driver.find_element_by_class_name("sub").click();  # 点击登录按钮
            # self.driver.find_element_by_id("submit").click()        #点击登录按钮
            sleep(1)
            return self.driver

        except:
            Base.printErr("ERR--log_in方法中登录然之操作失败.")
            return None

    # 这个函数负责登录后验证登录结果是否满足期望的结果
    # status:登录的期望状态是：True:成功；False：失败
    # expectUser:登录成功的期望用户名
    # expectInfo：登录失败的期望提示信息
    def v_login(self, status, expectUser, expectInfo):
        rc = ""
        try:
            if status:  # 如果登录的期望结果是成功的
                # 从登陆成功的界面上获取用户名

                userLogin = self.driver.find_element_by_css_selector \
                    ("ul[class='nav']>li>a").text
                # 如果从界面上获取的用户名和期望的用户名相等
                if userLogin.find(expectUser) > -1:
                    rc = "PASS--登录成功：" + expectUser  # 返回验证成功信息
                else:
                    # 返回验证失败信息
                    rc = "FAIL--登录错误，期望用户为‘%s’,实际用户为‘%s’" \
                         % (expectUser, userLogin)
            else:  # 如果登录的期望结果是失败的
                # 获取登录失败提示框中的提示信息
                errBoxMsg = self.driver.find_element_by_class_name("bootbox-body").text
                # 如果界面上获取的错误提示信息和期望的错误提示信息相等
                if errBoxMsg == expectInfo:
                    rc = "PASS--预期的登录错误提示信息验证成功！"  # 返回验证成功信息
                else:  # 否则不相等
                    # 返回验证失败信息
                    rc = "FAIL--登录验证失败，期望错误信息为‘%s’，实际错误信息为‘%s’" \
                         % (expectInfo, errBoxMsg)
        except:
            Base.printErr("ERR--v_login方法验证登陆时失败")
            return rc

            # raise rc
        # self.close_driver()       #关闭浏览器
        self.screen_shot("登录后校验")
        return rc  # 将验证成功、失败、错误等信息返回给调用者

    def screen_shot(self, suffix):
        timestamp = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
        self.driver.save_screenshot(self.web_screenshot_dir + os.sep + timestamp + "_" + suffix + ".png")

    def click_quickApp_link(self):
        sleep(2)
        link_quickApp = self.driver.find_element_by_link_text("快应用审核")
        link_quickApp.click()

    def submit_faile(self, pkg_info):
        try:
            pkg_name, pkg_version = self.click_check_link(pkg_info)
            self.driver.find_element_by_id("combox_result_id").click()
            self.driver.find_element_by_xpath("//a[text()='不通过']").click()
            self.driver.find_element_by_id("combox_reason_id").click()
            self.driver.find_element_by_xpath("//a[text()='应用无法正常运行或功能存在问题']").click()
            self.driver.find_element_by_id("remarks").send_keys("自动化测试")
            self.driver.find_element_by_xpath("//button[text()='提交']").click()
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element_by_xpath("//div[text()='提交成功']"))
            sleep(3)
            logger.error("‘" + pkg_name + "'审核不通过!")
        except:
            logger.error(Base.printErr("pkg_name=" + pkg_name + " & " +pkg_version+"  审核失败!"))
        self.screen_shot("审核不通过")

    def submit_success(self, pkg_info):
        try:
            pkg_name, pkg_version = self.click_check_link(pkg_info)
            self.driver.find_element_by_xpath("//button[text()='提交']").click()
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element_by_xpath("//div[text()='提交成功']"))
            sleep(3)
            # submit_rs = self.driver.find_element_by_xpath("//div[text()='提交成功']")
            # submit_txt = submit_rs.text
            # logger.info("submit_txt = '" + submit_txt + "'")
            logger.info("'" + pkg_name + "'审核通过!")
        except:
            logger.error(Base.printErr("pkg_name=" + pkg_name + " & " +pkg_version+"  审核失败!"))
        self.screen_shot("审核通过")

    def click_check_link(self, pkg_info):
        pkg_name = pkg_info[1]
        pkg_id = pkg_info[0]
        pkg_version = pkg_info[2]
        self.driver.find_element_by_name("_search[rpkPackage]").send_keys(pkg_name)
        Select(self.driver.find_element_by_id("rpk_status")).select_by_visible_text("审核中")
        self.driver.find_element_by_id("veryfy2_sub").click()
        sleep(2)
        pkg_id_nodes = self.driver.find_elements_by_xpath("//td[@class='package']/preceding-sibling::td[2]")
        for i in range(len(pkg_id_nodes)):
            pkg_id_node = pkg_id_nodes[i]
            id_str = pkg_id_node.text
            if int(id_str) == int(pkg_id):
                j = i + 1
                self.driver.find_element_by_xpath(
                    "//*[@id=\"navTab\"]/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr[" + str(
                        j) + "]/td[8]/a[1]").click()
                sleep(2)
                break
        return pkg_name, pkg_version

    def syn_server(self, pkg_info):
        try:
            pkg_name = pkg_info[1]
            pkg_id = pkg_info[0]
            pkg_version = pkg_info[2]
            self.driver.find_element_by_name("_search[rpkPackage]").send_keys(pkg_name)
            Select(self.driver.find_element_by_id("rpk_status")).select_by_visible_text("已上架")
            self.driver.find_element_by_id("veryfy2_sub").click()
            sleep(2)
            self.click_syn_link(pkg_id)
            for i in range(3):
                if self.syn_fail_again_syn(pkg_id):
                    break

            sleep(3)
            logger.info("'" + pkg_name + "'同步成功!")

        except:
            logger.error(Base.printErr("pkg_name=" + pkg_name + " & " +pkg_version+"  同步失败!"))
        self.screen_shot("同步")

    def syn_fail_again_syn(self, pkg_id):
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element_by_xpath("//div[text()='同步成功']"))
            return True
        except:
            self.click_syn_link(pkg_id)
            return False

    def click_syn_link(self, pkg_id):
        pkg_id_nodes = self.driver.find_elements_by_xpath("//td[@class='package']/preceding-sibling::td[2]")
        for i in range(len(pkg_id_nodes)):
            pkg_id_node = pkg_id_nodes[i]
            id_str = pkg_id_node.text
            if int(id_str) == int(pkg_id):
                j = i + 1
                self.driver.find_element_by_xpath(
                    "//*[@id=\"navTab\"]/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr[" + str(
                        j) + "]/td[8]/a[3]").click()
                sleep(2)
                break

    def has_need_check_app(self):
        Select(self.driver.find_element_by_id("rpk_status")).select_by_visible_text("审核中")
        self.driver.find_element_by_id("veryfy2_sub").click()
        text = self.driver.find_element_by_xpath(
            "//*[@id=\"navTab\"]/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[8]/a[1]").text
        if text == "审核":
            return True
        else:
            return False
        self.screen_shot("是否还存在未审核app")

    def get_page_pkg_names(self,not_test_app_num):
        pkg_info = []
        if not_test_app_num >0 and not_test_app_num % 10 ==0:
             logger.info("not_test_app_num="+str(not_test_app_num)+",点击下一页")
             self.driver.find_element_by_xpath("//span[text()='下一页']").click()
             sleep(2)

        Select(self.driver.find_element_by_id("rpk_status")).select_by_visible_text("审核中")
        self.driver.find_element_by_id("veryfy2_sub").click()
        sleep(3)
        # 获取当前页面所有待审核的包名称
        pkg_ids= []
        pkg_id_nodes =self.driver.find_elements_by_xpath("//td[@class='package']/preceding-sibling::td[2]")
        for pkg_id_node in pkg_id_nodes:
            pkg_id = pkg_id_node.text
            pkg_ids.append(pkg_id)
        print(pkg_ids)
        pkg_names= []
        pkg_name_nodes =self.driver.find_elements_by_xpath("//td[@class='package']")
        for pkg_name_node in pkg_name_nodes:
            pkg_name = pkg_name_node.text
            pkg_names.append(pkg_name)
        print(pkg_names)
        pkg_versions =[]
        pkg_version_nodes =self.driver.find_elements_by_xpath("//td[@class='package']/following-sibling::td[1]")
        for pkg_version_node in pkg_version_nodes:
            pkg_version = pkg_version_node.text
            pkg_versions.append(pkg_version)
        print(pkg_versions)

        for i in range(len(pkg_ids)):
            pkg_id = pkg_ids[i]
            pkg_info.append([pkg_id,pkg_names[i],pkg_versions[i]])
        # pkg_info = dict(zip(pkg_ids,pkg_names,pkg_versions))
        self.screen_shot("待审核包名列表")
        print(pkg_info)

        return pkg_info

    def confirm_rpk(self, pkg_info):
        pkg_name = pkg_info[1]
        pkg_id = pkg_info[0]
        Select(self.driver.find_element_by_id("rpk_status")).select_by_visible_text("审核中")
        self.driver.find_element_by_name("_search[rpkPackage]").send_keys(pkg_name)
        self.driver.find_element_by_id("veryfy2_sub").click()

        pkg_id_nodes =self.driver.find_elements_by_xpath("//td[@class='package']/preceding-sibling::td[2]")
        for i in range(len(pkg_id_nodes)):
            pkg_id_node = pkg_id_nodes[i]
            id_str = pkg_id_node.text
            if int(id_str) == int(pkg_id):
                 j = i+1
                 self.driver.find_element_by_xpath(
            "//*[@id=\"navTab\"]/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j)+"]/td[8]/a[1]").click()
                 sleep(2)
                 break
                 # print(special_app.text)
                 # exit(1)

            # pkg_ids.append(pkg_id)
        # text = self.driver.find_element_by_xpath(
        #     "//*[@id=\"navTab\"]/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[8]/a[1]").text
        # if text == "详情":
        #     self.driver.find_element_by_xpath("//span[text()='同步']").click()
        #     sleep(2)
        #     self.driver.find_element_by_xpath("//span[text()='确定']").click()
        # elif text == "审核":
        #     self.driver.find_element_by_xpath(
        #         "//*[@id=\"navTab\"]/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[8]/a[1]").click()
        # sleep(2)
        # pkg_name = self.driver.find_element_by_xpath("/html/body/div[16]/div[2]/div/div/form/div[1]/div[1]/span").text
        # print(pkg_name)
        # rs.append(pkg_name)
        download_addr = self.driver.find_element_by_class_name("softdown").get_attribute("href")
        print(download_addr)
        r = requests.get(download_addr)
        savePath =self.app_download_dir
        fileName = download_addr.split("/")[-1]
        print(fileName)
        filePath = os.path.join(savePath, fileName)
        with open(filePath, "wb") as file:
            file.write(r.content)
        # cmd = "adb push "+filePath+" /sdcard/rpks/"
        # logger.info(Util.exccmd(cmd))
        # rs.append(filePath)
        self.screen_shot("审核之前的下载")
        return filePath

    def push_apk(self, serial, filePath):
        cmd = "adb -s " + serial + " push " + filePath + " /sdcard/rpks/"
        logger.info(Util.exccmd(cmd))

    def submit(self):
        self.driver.find_element_by_xpath("//button[text()='提交']").click()

    def close_browser(self):
        self.close_driver()


def sucess_login(screenshot_dir):
    global rzLogin, x
    web_screenshot_dir = screenshot_dir + os.sep + "web"
    if not os.path.exists(web_screenshot_dir):
        os.mkdir(web_screenshot_dir)
    rzLogin = RanzhiLogin(web_screenshot_dir)  # 实例化上面的然之登录类
    print("-- testcase_01 正确的用户名密码 --")  # 打印提示当前用例名称
    rzLogin.log_in("autotest", "autotest123")  # 调用类方法用正确的用户名admin密码111111登录然之
    x = rzLogin.v_login(True, "齐梅秀", "")
    print(x)  # 调用类方法验证登录后的结果检查点
    rzLogin.click_quickApp_link()
    return rzLogin


def init_screenshot_dir():
    rootLogDir = Base.get_cur_dir(__file__)
    currentLogDirName = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    currentTimeStampLogDir = os.path.join(rootLogDir, currentLogDirName)
    os.mkdir(currentTimeStampLogDir)
    return currentTimeStampLogDir


def clear_data():
    cmd_clear_data = "adb -s " + serial + " shell pm clear com.gionee.agileapp"
    logger.info(cmd_clear_data)
    cmd_str = Util.exccmd(cmd_clear_data)
    logger.info(cmd_str)


# 下面写几个测试用例来调用上述函数做测试
if __name__ == "__main__":
    # serial = "IZEAMF6LLJVSLNQC"
    Util.finddevices()
    serial = input("请输入被测试手机串号:\n ********************** \n eg:CYHAVCYLEULJB6FU \n **********************\n请输入:")
    logger.info("被测手机串号:"+serial)
    cmd = "pip install uiautomator2"
    cmd_str =Util.exccmd(cmd)
    logger.info(cmd_str)
    time.sleep(5)
    cmd = "python -m uiautomator2 init"
    cmd_str = Util.exccmd(cmd)
    logger.info(cmd_str)
    time.sleep(5)
    not_test_apps = []
    screenshot_dir = init_screenshot_dir()
    cmd = "adb -s " + serial + " shell date +%s"
    start_stamp = Util.exccmd(cmd)
    logger.info("start_stamp=" + start_stamp)
    clear_data()
    i = 0
    while True:
        rzLogin = sucess_login(screenshot_dir)
        pkg_list = rzLogin.get_page_pkg_names(len(not_test_apps))
        rzLogin.close_browser()
        for pkg_info in pkg_list:
            try:
                # print(not_test_apps)
                pkg_name = pkg_info[1]
                pkg_version = pkg_info[2]
                is_test = True
                for not_test_app in not_test_apps:
                    if not_test_app.__contains__(pkg_name) and not_test_app.__contains__(pkg_version):
                        is_test = False
                        break
                if not is_test:
                    continue
                logger.info("pkg_name=" + str(pkg_info) + " 开始测试!")
                rzLogin = sucess_login(screenshot_dir)

                apk_download_addr = rzLogin.confirm_rpk(pkg_info)
                rzLogin.push_apk(serial, apk_download_addr)
                sleep(3)
                rzLogin.close_browser()
                rs = smok_test.main(serial,pkg_name,screenshot_dir)
                logger.info("**********"+pkg_name+" & "+pkg_version+"************手机端测试结束")
                if rs == Config.NOT_NEED_TEST_CODE:
                    not_test_apps.append([pkg_name,pkg_version])
                    logger.info("已下架APP:" + str(not_test_apps))
                    continue
                rzLogin = sucess_login(screenshot_dir)
                if rs == Config.TEST_PASS_CODE:
                    # 审核通过
                    rzLogin.submit_success(pkg_info)
                    rzLogin.close_browser()
                    # 同步
                    rzLogin = sucess_login(screenshot_dir)
                    print("开始同步")
                    print(pkg_info)
                    print(pkg_name)
                    rzLogin.syn_server(pkg_info)


                else:
                    rzLogin.submit_faile(pkg_info)
                rzLogin.close_browser()
            except:
                logger.error(Base.printErr("pkg_name=" + pkg_name + " & " +pkg_version+"  测试失败!"))
        rzLogin = sucess_login(screenshot_dir)
        is_has_need_check_app = rzLogin.has_need_check_app()
        rzLogin.close_browser()
        if not is_has_need_check_app:
            break
        i += 1
    cmd = "adb -s " + serial + " shell date +%s"
    end_stamp = Util.exccmd(cmd)
    logger.info("end_stamp=" + end_stamp)
    dump_info = dump_crash_info(serial, int(start_stamp), int(end_stamp))
    filename = screenshot_dir + os.sep + 'crash_data.txt'
    with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        f.write(dump_info)









        # print("-- testcase_02 错误的用户名密码 --")
        # rzLogin.log_in("abcd", "222222")
        # print(rzLogin.v_login(False, "", "登录失败，请检查您的成员名或密码是否填写正确。"))
        #
        # print("-- testcase_03 空的用户名/密码 --")
        # rzLogin.log_in("cdef", "")
        # print(rzLogin.v_login(False, "", "登录失败, 用户名或密码不能为空"))
