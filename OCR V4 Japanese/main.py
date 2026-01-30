import subprocess
import multiprocessing

def run_node():
    subprocess.run(["node", "OCR_V4_Japanese/server.js"])

def Run_OCR():
    subprocess.run(["python3", "OCR_V4_Japanese/OCR_V4.py"])

def run_position1():
    subprocess.run(["python3", "OCR_V4_Japanese/FP.py"])

def run_position2():
    subprocess.run(["python3", "OCR_V4_Japanese/SP.py"])

if __name__ == "__main__":

    thread_node = multiprocessing.Process(target=run_node)
    thread_ocr = multiprocessing.Process(target=Run_OCR)
    thread_position1 = multiprocessing.Process(target=run_position1)
    thread_position2 = multiprocessing.Process(target=run_position2)


    thread_node.start()
    thread_ocr.start()
    thread_position1.start()
    thread_position2.start()


