import socketio
import threading
import keyboard
import os
import pyautogui
from pynput import keyboard
import logging
from PIL import Image
from manga_ocr import MangaOcr
import eventlet
import mss
import socketio
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
cli = socketio.Client()
mocr = MangaOcr()
import requests
cli.connect('http://localhost:5000')

x1 = 0
y1 = 0
x2 = 0
y2 = 0

logging.basicConfig(level=logging.WARNING)

@sio.event
def roi_control_x(sid, data):
    global x1, y1
    X1,Y1 = pyautogui.position()
    x1 = X1
    y1 = Y1
@sio.event
def roi_control_y(sid, data):
    global x2, y2
    X2,Y2 = pyautogui.position()
    x2 = X2
    y2 = Y2

def server():

    eventlet.wsgi.server(eventlet.listen(('localhost', 3000)), app)


def process_screenshots():
    with mss.mss() as sct:
      sct.shot(output="cap.png")

    

    try:
        roi = (x1, y1, x2, y2)
        print("First Screenshot Taken")
        screenshot_pil1 = Image.open("cap.png")
        screenshot = screenshot_pil1.crop(roi)
        gray = screenshot.convert("L")
        japanese = mocr(gray)
        os.remove("cap.png")
        print("Text traslated")
        extracted_text = japanese
        if extracted_text:
         cli.emit('transferControl', {'message': extracted_text})
 
         
         
    except Exception as e:
        print(f"Error processing screenshot: {e}")

server_thread = threading.Thread(target=server)
server_thread.start()
key_to_process = keyboard.KeyCode.from_char('w')
with keyboard.Listener(on_press=lambda key: process_screenshots() if key == key_to_process else None) as listener:
    print(f"Press '{key_to_process}' to process screenshots. Press 'esc' to exit.")
    listener.join()
