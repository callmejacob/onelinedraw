
# onelinedraw
wx game - 一笔画猫猫的研究 (mac平台，android)


# c++: findpath
首先进入cpp目录中，执行以下命令:

cd cpp

cmake .

make

编译出的findpath执行程序，用于脚本寻找正确的路径

# 脚本执行: shell

首先进入一张地图中，执行:

./oneline.sh

这个脚本会调用同目录下的oneline.py共计15次，因为一个猫猫有15个地图，这样可以一次性闯关。

注意最后一行

os.system('adb shell input tap 720 1500')

是为了在一张地图结束后，点击按钮直接进入下一张地图，这里的(720,1500)需要根据手机按钮的位置做适配，暂时还没有做图像自动识别。
