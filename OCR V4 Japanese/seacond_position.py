from pynput import keyboard
import socketio
import pyautogui

sio = socketio.Client()
sio.connect('http://localhost:3000')

def sety():
    try:

        sio.emit('roi_control_y', {"start":"go"})
         
    except Exception as e:
        print(f"Error in sety: {e}")
        if not sio.connected:
           
            sio.connect('http://localhost:3000')
    



key_to_process = keyboard.KeyCode.from_char('e')
with keyboard.Listener(on_press=lambda key: sety() if key == key_to_process else None) as listener:
    print(f"Press '{key_to_process}' to process screenshots. Press 'esc' to exit.")
    listener.join()
