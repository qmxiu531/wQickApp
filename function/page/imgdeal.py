# -*- coding: utf-8 -*-
__author__ = 'suse'
import urllib3,base64
from urllib.parse import urlencode
urllib3.disable_warnings()
access_token='24.c06a31b78d57ba3a4129c6e7a5713adc.2592000.1534390002.282335-11545175'
http=urllib3.PoolManager()
url='https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token='+access_token
f = open('F:/demo.jpg','rb')
#参数image：图像base64编码
img = base64.b64encode(f.read())
params={'image':img}
#对base64数据进行urlencode处理
params=urlencode(params)
request=http.request('POST',
                      url,
                      body=params,
                      headers={'Content-Type':'application/x-www-form-urlencoded'})
#对返回的byte字节进行处理。Python3输出位串，而不是可读的字符串，需要进行转换
result = str(request.data,'utf-8')
print(result)
if(result.find("取消")>-1 and result.find("确定")>-1):
    print("===============")

