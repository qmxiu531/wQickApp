# -*- coding: utf-8 -*-
import subprocess
import time
from function.utils import Util
__author__ = 'suse'
logger = Util.logger

class Traffic:
    def __init__(self,serial,uid):
        self.serial = serial
        self.uid = uid

    def get_app_traffic(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        traffic_initial = [0]*16
        traffic_prefix = []
        getTrafficcmd = 'adb -s '+self.serial+' shell cat /proc/net/xt_qtaguid/stats | grep ' + str(self.uid)

        p = subprocess.Popen(getTrafficcmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            line = str(line, encoding='utf-8')
            ll = line.strip()
            ll2=ll.replace(' ',',')
            ll2_list=ll2.split(',')
            traffic_list = ll2_list[5:]
            traffic_prefix = ll2_list[0:4]
            traffic_list_int = [int(e) for e in traffic_list]

            traffic_initial = [x+y for x, y in zip(traffic_initial, traffic_list_int)]
            #print traffic_list
            # print(currentTime + "," + ll2)
        retval = p.wait()
        total_traffic = traffic_initial[1] + traffic_initial[3]
        # print(traffic_initial)
        traffic_list_str = [str(e) for e in traffic_initial]
        # print(traffic_prefix + traffic_list_str)
        traffic = ','.join(traffic_prefix + traffic_list_str)
        # print(currentTime +','+ traffic)
        logger.info(currentTime +','+ traffic + '\n')
        logger.info(currentTime +','+ str(total_traffic) + '\n')
        return total_traffic

