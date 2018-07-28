# -*- coding: utf-8 -*-
import os,sys
from function.utils import Log
import logging
import threading
import multiprocessing
import time
import glob,re
import subprocess
import itertools

logger = Log.Logger('report.log',clevel = logging.DEBUG,Flevel = logging.INFO)

def anyTrue(predicate, sequence):
    return True in map(predicate, sequence)

def filterFiles(folder, exts,isDeep=False):
    findFileList = []
    for fileName in os.listdir(folder):
        # print(fileName)
        if(isDeep ==True):
            if os.path.isdir(folder + os.sep + fileName):
                filterFiles(folder + os.sep + fileName, exts)
            elif anyTrue(fileName.endswith, exts):
                findFileList.append(fileName)
        elif anyTrue(fileName.endswith, exts):
            findFileList.append(fileName)
    return findFileList

def exccmd(cmd):
    try:
        #os.popen(cmd).read()
        return subprocess.getoutput(cmd)
    except Exception:
        return None

#遍历目录内的文件列表
def listFile(path, isDeep=True):
    _list = []
    if isDeep:
        try:
            for root, dirs, files in os.walk(path):
                for fl in files:
                    _list.append('%s\%s' % (root, fl))
        except:
            pass
    else:
        for fn in glob.glob( path + os.sep + '*' ):
            if not os.path.isdir(fn):
                _list.append('%s' % path + os.sep + fn[fn.rfind('\\')+1:])
    return _list

def listChildDir(path):
    _list = []
    for fn in glob.glob(path+os.sep+"*"):
        if os.path.isdir(fn):
            _list.append('%s' % fn[fn.rfind('\\')+1:])
    return _list


def finddevices():
        rst = exccmd('adb devices')
        devices = re.findall(r'(.*?)\s+device',rst)
        if len(devices) > 1:
            deviceIds = devices[1:]
            logger.info('共找到%s个手机'%str(len(devices)-1))
            for i in deviceIds:
                logger.info('ID为:%s'%i)
            return deviceIds
        else:
            logger.error('没有找到手机，请检查')





#线程函数
class FuncThread(threading.Thread):
    def __init__(self, func, *params, **paramMap):
        threading.Thread.__init__(self)
        self.func = func
        self.params = params
        self.paramMap = paramMap
        self.rst = None
        self.finished = False

    def run(self):
        self.rst = self.func(*self.params, **self.paramMap)
        self.finished = True

    def getResult(self):
        return self.rst

    def isFinished(self):
        return self.finished

def doInThread(func, *params, **paramMap):
    t_setDaemon = None
    if 't_setDaemon' in paramMap:
        t_setDaemon = paramMap['t_setDaemon']
        del paramMap['t_setDaemon']
    ft = FuncThread(func, *params, **paramMap)
    if t_setDaemon != None:
        ft.setDaemon(t_setDaemon)
    ft.start()
    return ft
