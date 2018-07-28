# -*- coding: utf-8 -*-
import subprocess
import time
fo = open(r"D:\foo.txt", "w")
#获取进程ID
getProcessIdcmd = 'adb shell ps | grep com.gionee.agileapp$'
p = subprocess.Popen(getProcessIdcmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
content = p.stdout.readlines()
print(content)
print("&&&&&")
print(type(content))
print("&&&&&")
if len(content) == 1:
    processId = content[0].split()[1]
else:
    print("not get processID")
#获取进程对应的UID
print(int(processId))
getUidcmd = 'adb shell cat /proc/' + str(int(processId)) + '/status | grep Uid'
print("***"+getUidcmd)
p = subprocess.Popen(getUidcmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
content = p.stdout.readlines()
print(type(content[0]))
uidStr = str(content[0], encoding='utf-8')
print(uidStr)
uidList = uidStr.strip().split('\t')
print("====")
print(uidList)
print("====")
uid = uidList[1]
print(uid)

#获取UID对应的Traffic
getTrafficcmd = 'adb shell cat /proc/net/xt_qtaguid/stats | grep ' + uid

for i in range(10000):
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    traffic_initial = [0]*16
    traffic_prefix = []
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
        print(currentTime + "," + ll2)
    retval = p.wait()
    print(traffic_initial)
    traffic_list_str = [str(e) for e in traffic_initial]
    print(traffic_prefix + traffic_list_str)
    traffic = ','.join(traffic_prefix + traffic_list_str)
    print(currentTime +','+ traffic)
    fo.write(currentTime +','+ traffic + '\n')
    time.sleep(60)
    print('--------------')
fo.close()
