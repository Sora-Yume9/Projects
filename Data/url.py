import pandas as pd
import glob
import ast
import requests
import time
from bs4 import BeautifulSoup
import threading


path = r"C:\Users\conta\.cache\kagglehub\datasets\csutliff1\ao3-dataset-collected-4-oct-2025\versions\4"
path_to_file = r"C:\Projects\Data_2.txt"
path_to_file_2 = r"C:\Projects\test.txt"
path_to_file_3 = r"C:\Projects\Data_3.txt"
# Load files
files = glob.glob(f"{path}/*")
fd = pd.read_csv(files[3], encoding="utf-8") 


def scrap(start,end,file_path):
    session = requests.Session()
    index = start
    for i in range(start, end):

        tag = fd.loc[i, "Fandom Tags"]
        page = fd.loc[i, "URL"]
        tags_list = ast.literal_eval(tag)

        retries = 3
        for attempt in range(retries):
            try:
                
                response = session.get(page+"?view_adult=true")
                #time.sleep(3)
                response.encoding = 'utf-8'

                if response.status_code in [403, 404]:
                    print(f"Got {response.status_code} for {page}")
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                div = soup.find("div", class_="userstuff")
                if div:
                    paragraphs = div.find_all("p")
                    all_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
                    with open(file_path, "a", encoding="utf-8", errors="replace") as file:
                        file.write(f"\n\n=== fandom: {tags_list[0]} === \n\n{all_text} \n\n ---END OF WORK---\n")
                    print(f"Works Taken: {index}")
                    index += 1
                    break  
                else:
                    print(f"Attempt {attempt+1}: Div not found, retrying...")
                    print(page)
                    time.sleep(10)
                    continue  

            except Exception as e:
                print(f"Error on {page}: {e}")
                time.sleep(5) 
                continue
thread1 = threading.Thread(target=scrap, args=(23333,46000,path_to_file))
thread2 = threading.Thread(target=scrap, args=(68812,82000,path_to_file_2))
thread3 = threading.Thread(target=scrap, args=(87517,92000,path_to_file_3))
# Start threads
thread1.start()
thread2.start()
thread3.start()
# Wait for threads to finish
thread1.join()
thread2.join()
thread3.join()


