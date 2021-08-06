# Google Dino Bot

import time
import webbrowser
import numpy as np
import pyautogui

url = "www.chromedino.com/"
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
webbrowser.get(chrome_path).open(url) 

time.sleep(3)
pyautogui.press('space')

while True:
	screen = pyautogui.screenshot()
	image = np.array(screen)
	avg_pixel_sum = np.sum(image[220:270, 510:560]) / 2500
	if avg_pixel_sum >= 105:
		pyautogui.press('space')