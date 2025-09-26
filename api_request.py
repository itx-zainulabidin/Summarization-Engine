import os
import requests

url = "http://127.0.0.1:8000/api/summarize"

data_folder = "./data"   # change if needed
files = os.listdir(data_folder)  # gets all files in the folder
modes = ["tldr","short","extended"]

def call_api(files, modes):
    
    for file in files:
        for mode in modes:
            payload = {
                "doc_id": file,
                "mode": mode,
                "export": "pdf"
            }

            res = requests.post(url, json=payload)
            print("Status Code:", res.status_code)
            # print("Raw Response Text:", res.text)
            print("Response JSON:", res.json())
            # return res.json() 
    

call_api(files, modes)