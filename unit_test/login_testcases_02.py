# -*- coding: gbk -*-
import unittest         #���뵥Ԫ���Կ��
from function.page.login_page import *    #�����Զ���Ĺ��ò�����
from function.base.base import *
from function.base.base_page import *

class LoginTestCases2(unittest.TestCase):
    def setUp(self):                    #��ʼ������������ǰ������
        print("-- testcase start --")
        #ʵ����RanzhiLogin�࣬������URL
        self.rzLogin = RanzhiLogin()
        #����һ����Ա��������Ϊ��֤�Ƿ�ɹ��ı�ǩ
        self.succ = "PASS--"

    def tearDown(self): #������β����
        print("-- testcase finished --")

    def test_log_in_batch(self):
        #����������������ķ���
        #�������������������ݺ�ҵ���߼����룬���ｫ��¼�û����뵥�����嵽һ��csv�ļ��У�
        # ����ִ��Աֻ��Ҫά���ø����ݼ���
        #ҵ���߼������Զ��������Ա�ڲ��Գ�����ʵ�֣��ó����Զ����ö������������ļ���ɲ���
        #���ȴ򿪲��������ļ�
        ex = g_dicFun.get("excel")
        cases = ex.get_page_data("login")
        x = 0   #����һ��������������ʶ�������ļ��еĵ�һ��
        fNum = 0            #ʧ�ܵ�������
        cNum = 0            #��������
        for case in cases:    #ѭ����ά���飬ÿѭ��һ��ȡ��һ�����ݣ�һά���飩
            if x == 0:                          #����ǵ�һ�У���һ��ѭ����
                x += 1
                continue

            print("-- testcase��%s --"%case[0])   #��ӡ������������user[0]�������Ļ
            self.rzLogin.log_in(case[1], case[2])   #���ù��ú���ִ�е�¼Ȼ֮
            if case[4] == "":                   #�������������ǿյģ���ô���õڶ���
                case[4]=case[1]
            rc = self.rzLogin.v_login(case[3], case[4], case[4])#���ù��ú���ִ�е�¼����֤
            try:
                res = "Pass"                #������Ϊ�������ǳɹ���
                msg = ""
                self.assertIn(self.succ, rc) #����֤�Ľ�����ж���һ���Ƿ�ɹ�������'PASS--'��Ϊ�ɹ���
            except:          #���������except�Ӿ����ʾ��������֤ʧ��
                res = "Failed"              #������ʧ����
                msg = rc                #��¼ʧ�ܵĴ�����Ϣ
                Base.printErr()                   #��ʧ�ܵ���Ϣ��ӡ����Ļ
                fNum = fNum + 1
            #�����д�뵽user_login_res.csv��
            cNum = cNum + 1
            ex.write_by_index(x, 5, "login", res)
            ex.write_by_index(x, 6, "login", msg)
            x += 1
            ex.save_excel()
        #�������allMsg����������Ϊ���������д���ʧ�ܵ��������׳�������Ϣ
        self.assertEqual(fNum, 0, "��������:%d,ʧ��������:%d."%(cNum, fNum))