# 快应用自动审核工具 #

### 前提条件 ###
1、PC需要安装adb,python3
2、被测手机版本支持快应用
3、被测手机与PC的adb连接正常

### 使用方法 ###
1. 选择需要测试的用例，输入需要测试的次数(不输入就是默认的测试次数)；
2. 点击开始后自动测试；
3. 完成后自动跳转到测试结果界面
4. 测试结果界面可以发送邮件和查看测试的详情



### 模块划分 ###
1.app模块 - 主apk部分，界面的实现和调用case
> 1.main 公共的包模块
>
> 2.pressure 品质压力测试的分包
>
> 3.project 项目压力测试的分包(原monkeyrunner脚本)
>
> 4.instrument 器械压力测试的分包

2.pressure模块 - case部分
>androidTest包：
>
>1.hardware_case 器械压力测试的case
>
>2.pressure_case 品质压力测试的case
>
>3.project_case 项目压力测试的case

3.install模块 - 一个辅助apk 用于安装和卸载apk操作


4.平台执行
    1.安装apk

    2.启动这个apk
    adb shell am start -n com.gionee.pressureTest/com.gionee.pressureTest.activity.HomeActivity

    3.发送广播
    adb shell am broadcast -a com.gionee.pressureTest.first  --ei type 0  --ei casecount 1  --ei count 2  --ez useaddress false  --ez islab true  --es address 'pengbeilin@gionee.com'

    type（int） 测试类型 -> 0 场景压力测试,1 单功能压力测试,2 器件压力测试

    casecount （int） 执行多少条case

    count （int）每条case执行多少次

    useaddress （boolean）是否用默认收件人 （测试的时候不用这个参数或者用false）

    address （String）增加的额外收件人

