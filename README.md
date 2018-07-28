#  快应用自动审核工具  #

### 前提条件 ###
1. PC需要安装adb,python3;
2. 被测手机版本支持快应用;
3. 被测手机与PC的adb连接正常;

### 使用方法 ###
#### 1.测试步骤: ####
> 1、点击quickTest.exe，输入被测手机串号
>
> 2、在测试过程中会截图
>
  ```
   > 1）当前时间戳                                          --总截图文件夹
   >
   > 2）当前时间戳->web                                     ---web平台自动化截图
   >
   > 3) 当前时间戳->mobile                                  ---被测手机自动化截图
   >
   > 4) 当前时间戳->mobile->white_screenshot                ---白屏截图
   >
   > 5) 当前时间戳->mobile->black_screenshot                ---黑屏截图
   > 
   > 6) 当前时间戳->mobile->screenshot_video_not_play       ---视频无法播放截图
   >
   > 7) 当前时间戳->mobile->screenshot_error_dir            ---快应用出现错误的截图
   ```

3、系统报错
   当前时间戳->crash_data.txt


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

