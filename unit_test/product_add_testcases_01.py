# -*- coding: gbk -*-
import csv              #����csv��
import unittest         #���뵥Ԫ���Կ��

from function.page.product_page import *     #�����Զ���Ĺ��ò�����
from function.base.comm_db import CommonDB   #�����Զ����Ȼ֮���ݿ������


class ProductAddTestCases1(unittest.TestCase):
    def setUp(self):#��ʼ������������ǰ������
        print("-- testcases start --")
        self.rzProduct = RanzhiProduct()
        self.m_db = self.rzProduct.rzDB
        self.succ = "PASS--"

    def tearDown(self): #������β����
        print("-- testcases finished --")


    def test_product_add_batch(self):
        #����������������ķ���
        #�������������������ݺ�ҵ���߼����룬���ｫ��¼�û����뵥�����嵽һ��csv�ļ��У�
        # ����ִ��Աֻ��Ҫά���ø����ݼ���
        #ҵ���߼������Զ��������Ա�ڲ��Գ�����ʵ�֣��ó����Զ����ö������������ļ���ɲ���
        ex = g_dicFun.get("excel")
        cases = ex.get_page_data("productAdd")
        x = 0
        nCount = 0  #����ִ�е���������
        nFail = 0   #����ʧ��������
        for case in cases:
            if x == 0:                          #����ǵ�һ�У���һ��ѭ����
                x += 1
                continue
            print("-- testcase��%s --"%case[0])                 #��ʼһ�ݲ���������ִ��
            try:
                self.rzProduct.log_in(g_dicRanzhi.get("user"), g_dicRanzhi.get("password"))
                case[7] =  ex.str_parse_func(case[7])   #ǰ��SQL
                case[8] = ex.str_parse_func(case[8])    #��֤SQL
                dbrc = self.m_db.execSql(case[7])
                if dbrc[0] == False:   #ִ��SQL������Ĵ���
                   print(dbrc[1])
                self.rzProduct.ranzhi_product_add(case)      #���ù��ú���ִ�в�Ʒ���
                rc = self.rzProduct.ranzhi_product_add_v(case)         #���ù��ú���ִ�е�¼����֤
                res = "Pass"                #������Ϊ�������ǳɹ���
                msg = ""
                self.assertIn(self.succ, rc) #����֤�Ľ�����ж���һ���Ƿ�ɹ�������'PASS--'��Ϊ�ɹ���
            except:          #���������except�Ӿ����ʾ��������֤ʧ��
                res = "Failed"              #������ʧ����
                msg = Base.printErr()
                nFail += 1
                #��ͼ
                #self.rzProduct.getDriver().save_screenshot("c:\\screenshot.jpg")
            nCount += 1
            #�����д�뵽���Excel��
            ex.write_by_index(x, 9, "productAdd", res)
            ex.write_by_index(x, 10, "productAdd", msg)
            x += 1
            self.rzProduct.close_driver()
        #����ʧ���������Ƿ����0
        ex.save_excel()
        self.assertEqual(nFail, 0, "��ִ��������:%d;����ʧ��������:%d"%(nCount, nFail))
