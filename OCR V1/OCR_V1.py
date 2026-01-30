
import subprocess
from pynput import keyboard
import easyocr
import mss
from PIL import Image
import numpy as np
roi = (19, 160, 1100, 747)
ocr_reader = easyocr.Reader(['en'])

def process_screenshots():
    with mss.mss() as sct:
     sct.shot(output="screenshot.png")
    

    try:
        screenshot_pil = Image.open("screenshot.png")
        print("Screenshot Taken")
        cropped_screenshot = screenshot_pil.crop(roi)
        gray = cropped_screenshot.convert("L")
        cropped_screenshot = gray
        cropped_screenshot.save("capture.png")
        np_array = np.array(cropped_screenshot)
        results = ocr_reader.readtext(np_array)
        extracted_text = ' '.join([result[1] for result in results])
        extracted_text = extracted_text.replace('\n', ' ')
        extracted_text = extracted_text.replace('1', 'i')
        extracted_text = extracted_text.replace('$', 's')
        extracted_text = extracted_text.replace('5', 's')
        extracted_text = extracted_text.replace('0', 'o')
        print("Screenshot Finalized")
        if extracted_text:
            subprocess.run(["festival", "--tts"], input=extracted_text, text=True)
            print(extracted_text)
    except Exception as e:
        print(f"Error processing screenshot: {e}")

key_to_process = keyboard.KeyCode.from_char('`')

with keyboard.Listener(on_press=lambda key: process_screenshots() if key == key_to_process else None) as listener:
    print(f"Press '{key_to_process}' to process screenshots. Press 'esc' to exit.")
    listener.join()