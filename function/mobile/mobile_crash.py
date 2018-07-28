# -*- coding: utf-8 -*-
from function.utils import Util
import re,time
__author__ = 'suse'
logger = Util.logger

class Crash:

    def __init__(self,serial):
        self.serial = serial
        self.crash_info = ""

    def get_raw_crash_info(self):
        cmd = "adb -s "+self.serial+" shell dumpsys dropbox --print"
        self.crash_info = Util.exccmd(cmd)
        return self.crash_info

    def get_crash(self,start_time_stamp=None,end_time_stamp=None):
        start_end_index = [-1,-1]
        crash_times = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",self.crash_info)
        for item_time in crash_times:
            time_stamp = time.mktime(time.strptime(item_time,'%Y-%m-%d %H:%M:%S'))
            if (start_end_index[0] == -1) and (int(time_stamp)-int(start_time_stamp) >0):
                start_index = self.crash_info.find(item_time)
                start_end_index[0] = start_index

            if end_time_stamp is not None:
                if int(time_stamp)-int(end_time_stamp) >0:
                    end_index = self.crash_info.find(item_time)
                    start_end_index[1] = end_index
                    break
            else:
                start_end_index[1] = len(self.crash_info)
        target_crash_info = self.crash_info[start_end_index[0]:start_end_index[1]]

        return target_crash_info


def dump_crash_info(serial,start_timestamp,end_timestamp):
    crash_obj = Crash(serial)
    crash_obj.get_raw_crash_info()
    crash_info = crash_obj.get_crash(start_timestamp,end_timestamp)
    return crash_info


if __name__ == '__main__':
    crash_obj = Crash("IZEAMF6LLJVSLNQC")
    crash_obj.get_raw_crash_info()
    crash_info = crash_obj.get_crash(1531711487,1531767135)
    print(crash_info)
    # test_datetime = "2018-07-16 11:24:47 SYSTEM_BOOT 2018-07-17 02:52:15"
    # mat = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",crash_info)
    # for item in mat:
    #     print(item)
    #     time_stamp = time.mktime(time.strptime(item,'%Y-%m-%d %H:%M:%S'))
    #     diff = int(time_stamp)-1531711487
    #     print(diff)
    #     if diff >0:
    #         print("==========")
    #         print(item)
    #         index = crash_info.find(item)
    #         print("***************")
    #         print(index)
    #         print(crash_info[index:])
    #         break

    # print(mat.groups())
    # print(mat.group(0))
    # time_str = mat.group(0)
    # time_stamp = time.mktime(time.strptime(time_str,'%Y-%m-%d %H:%M:%S'))
    # print(time_stamp)

