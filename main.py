import os
import time
import numpy as np
import cv2
import pyautogui
from PIL import ImageGrab
import subprocess
import win32com.client
import win32gui

file_path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\原神\原神.lnk'
# 创建快捷方式对象
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(file_path)
# 获取真实目录
target_path = shortcut.TargetPath.replace('launcher.exe', '')
target_dir = os.path.join(target_path, 'Genshin Impact Game', 'YuanShen.exe')
print("原神目录", target_dir)
# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()
total_pixel = screen_height * screen_width
print("屏幕分辨率为", screen_height, "*", screen_width)
pyautogui.FAILSAFE = False
# 获取原神启动情况
process = len(os.popen('tasklist | findstr YuanShen.exe').readlines())
if process >= 1:
    print("原神已经启动")
else:
    while True:
        # 读取屏幕
        screenshot = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
        number_of_white_pix = np.count_nonzero(screenshot == [255,255,255])
        yuan_content = number_of_white_pix / total_pixel * 100
        print(yuan_content)
        # print("原神含量", yuan_content, "%")
        if yuan_content >= 200:
            white_image = np.ones(screenshot.shape, dtype=np.uint8) * 255
            subprocess.Popen(target_dir)
            cv2.namedWindow('window', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            while True:
                hwnd = win32gui.FindWindow(None, 'window')
                if hwnd:
                    shell.SendKeys('%')
                    win32gui.SetForegroundWindow(hwnd)
                    break
            for alpha in np.linspace(0, 1, 100):
                # 计算加权叠加后的图像
                blended = cv2.addWeighted(screenshot, 1 - alpha, white_image, alpha, 0)
                # 在窗口中显示图像
                cv2.imshow("window", blended)
                cv2.waitKey(5)
            while True:
                hwnd = win32gui.FindWindow(None, '原神')
                if hwnd:
                    shell.SendKeys('%')
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(10)
                    exit()


