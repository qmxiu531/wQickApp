# -*- coding: utf-8 -*-
from function.utils import Util
from function.base.base import Base
__author__ = 'suse'
logger = Util.logger


class Device:
    def __init__(self,serial):
        self.serial = serial
    def check_device(self):
        rs = []
        try:
            cmd = "adb -s "+self.serial+" shell"
            logger.info(cmd)
            cmd_str = Util.exccmd(cmd)
            logger.info(cmd_str)
            if cmd_str.find("not found"):
                rs[0] = False
                rs[1] = cmd_str
            else:
                rs[0] = True
                rs[1] = cmd_str
        except:
            logger.error(cmd_str)
        return rs




