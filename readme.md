## AutoSmokeTest冒烟测试 ##

### 使用方法 ###

 >1.安装apk
 >2.首次进入apk的时候自动拉取测试用例列表,(连接一个内网的wifi,可能下载速度会比较慢)
 >3.菜单中有一个‘下载脚本’选项，点击下载脚本，下载成功之后再手动安装;
 >4.选择想要测试的模块或者部分用例,点击开始测试即可





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

