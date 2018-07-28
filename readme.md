# 压力测试 #

### 工具介绍 ###
![主界面](img/img_pressure.png)
![测试结果界面](img/img_result.png)
![发送邮件界面](img/img_mail.png)

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





前提条件：
1、PC需要安装adb,python3
2、被测手机版本支持快应用
3、被测手机与PC的adb连接正常

测试步骤：
1、点击quickTest.exe，输入被测手机串号
2、在测试过程中会截图
   1）当前时间戳                                          --总截图文件夹
   2）当前时间戳->web                                     ---web平台自动化截图
   3) 当前时间戳->mobile                                  ---被测手机自动化截图
   4) 当前时间戳->mobile->white_screenshot                ---白屏截图
   5) 当前时间戳->mobile->black_screenshot                ---黑屏截图
   6) 当前时间戳->mobile->screenshot_video_not_play       ---视频无法播放截图
   7) 当前时间戳->mobile->screenshot_error_dir            ---快应用出现错误的截图

3、系统报错
   当前时间戳->crash_data.txt

