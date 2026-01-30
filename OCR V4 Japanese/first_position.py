from pynput import keyboard
import socketio


sio = socketio.Client()

sio.connect('http://localhost:3000')
def setx():
    try:

        sio.emit('roi_control_x', {"start": "go"})
    except Exception as e:
        print(f"Error in setx: {e}")
        if not sio.connected:
            sio.connect('http://localhost:3000')
    



key_to_process = keyboard.KeyCode.from_char('q')
with keyboard.Listener(on_press=lambda key: setx() if key == key_to_process else None) as listener:
    print(f"Press '{key_to_process}' to process screenshots. Press 'esc' to exit.")
    listener.join()
