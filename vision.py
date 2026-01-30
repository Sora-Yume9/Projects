from pynput import keyboard
import mss
from PIL import Image
import pyautogui
import time
roi = (528, 159, 1000, 762)




def on_press(key):
    try:
        if key.char == '`':
            with mss.mss() as sct:
                sct.shot(output="screenshot.png")
            screenshot_pil = Image.open("screenshot.png")
            cropped_screenshot = screenshot_pil.crop(roi)
            gray = cropped_screenshot.convert("L")
            cropped_screenshot = gray
            cropped_screenshot.save("Pictures/Screenshots/capture.png")
            time.sleep(1)
            pyautogui.moveTo(300,144)
            time.sleep(0.5)
            pyautogui.dragTo(1176,360,duration= 0.8)
            time.sleep(2)
            pyautogui.moveTo(1170,612)
            pyautogui.click()
            time.sleep(2)
            pyautogui.scroll(-10)
            time.sleep(2)
            pyautogui.click()
            time.sleep(2)
            pyautogui.scroll(-1)
            time.sleep(1)
            pyautogui.moveTo(1100,628)
            time.sleep(0.5)
            pyautogui.click()
            pyautogui.moveTo(1100,603)
            time.sleep(0.5)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.moveTo(200,718)
            time.sleep(0.4)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.moveTo(648,712)
            time.sleep(0.7)
            pyautogui.click()

     
    except AttributeError:
        pass

# Set up the listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()