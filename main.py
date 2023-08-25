import os
import numpy as np
import cv2
import pyautogui
from PIL import ImageGrab
import subprocess
import win32com.client


def is_running(process_name):
    try:
        process = len(os.popen('tasklist | findstr ' + process_name).readlines())
        print(process)
        if process >= 1:
            return True
        else:
            print("原神已经启动")

    except:
        print("程序错误")


def check_yuan():
    global Running_statues
    # 读取屏幕
    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    number_of_white_pix = np.count_nonzero(screenshot >= 254)
    # print(number_of_white_pix)
    yuan_content = number_of_white_pix / total_pixel * 100
    # print("原神含量", yuan_content, "%")
    if yuan_content >= 95:
        Running_statues = 0


def YUANSHEN_QIDONG():
    subprocess.Popen(target_dir)


file_path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\原神\原神.lnk'
# 创建快捷方式对象
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(file_path)
# 获取真实目录
target_path = shortcut.TargetPath.replace('launcher.exe', '')
target_dir = os.path.join(target_path, 'Genshin Impact Game', 'YuanShen.exe')
print("原神目录", target_dir)
# 获取原神启动情况
Running_statues = is_running("YuanShen.exe")
Running_statues = 1
# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()
total_pixel = screen_height * screen_width
print("屏幕分辨率为", screen_height, "*", screen_width)
pyautogui.FAILSAFE = False

while Running_statues:
    check_yuan()

YUANSHEN_QIDONG()
