import time
import pyautogui

string = """हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादे व 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️ हर हर महादेव 🕉️"""
emoji = '\U0001F549'
emoji1= '\u0950'
string1 = f"har har mahadev {emoji1}"
time.sleep(2)
while True:
    time.sleep(2)
    pyautogui.click(1450, 760)
    # pyautogui.write(string)
    pyautogui.typewrite(string1, interval=0.1)
    pyautogui.press('enter')