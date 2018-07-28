# -*- coding: gbk -*-
import unittest         #���뵥Ԫ���Կ��

from function.page.contact_page import *     #�����Զ���Ĺ��ò�����
from function.base.comm_db import CommonDB   #�����Զ����Ȼ֮���ݿ������


class ContactAddTestCases1(unittest.TestCase):
    def setUp(self):#��ʼ������������ǰ������
        print("-- testcases start --")
        self.rzContact = RanzhiContact()
        self.m_db = self.rzContact.rzDB
        self.succ = "PASS--"

    def tearDown(self): #������β����
        print("-- testcases finished --")


    def test_contact_add_batch(self):
        #����������������ķ���
        ex = g_dicFun.get("excel")
        cases = ex.get_page_data("contactAdd")
        x = 0
        nCount = 0  #����ִ�е���������
        nFail = 0   #����ʧ��������
        for case in cases:
            if x == 0:                              #����ǵ�һ�У���һ��ѭ����
                x += 1
                continue
            print("-- testcase��%s --"%case[0])   #��ʼһ�ݲ���������ִ��
            try:
                self.rzContact.log_in(g_dicRanzhi.get("user"), g_dicRanzhi.get("password"))
                case[22] =  ex.str_parse_func(case[22])
                case[23] = ex.str_parse_func(case[23])
                dbrc = self.m_db.execSql(case[22])
                if dbrc[0] == False:   #ִ��SQL������Ĵ���
                   print(dbrc[1])
                self.rzContact.ranzhi_contact_add(case)      #���ù��ú���ִ�в�Ʒ���
                rc = self.rzContact.ranzhi_contact_add_v(case)         #���ù��ú���ִ�е�¼����֤
                res = "Pass"                #������Ϊ�������ǳɹ���
                msg = ""
                self.assertIn(self.succ, rc) #����֤�Ľ�����ж���һ���Ƿ�ɹ�������'PASS--'��Ϊ�ɹ���
            except:          #���������except�Ӿ����ʾ��������֤ʧ��
                res = "Failed"              #������ʧ����
                msg = Base.printErr()
                nFail += 1
                #��ͼ
                self.rzProduct.getDriver().save_screenshot("c:\\screenshot.jpg")
            nCount += 1
            #�����д�뵽���Excel��
            ex.write_by_index(x, 24, "contactAdd", res)
            ex.write_by_index(x, 25, "contactAdd", msg)
            x += 1
            self.rzContact.close_driver()
        #����ʧ���������Ƿ����0
        ex.save_excel()
        self.assertEqual(nFail, 0, "��ִ��������:%d;����ʧ��������:%d"%(nCount, nFail))
