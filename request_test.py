import requests

url = "http://127.0.0.1:8000/api/summarize"
payload = {
    "doc_id": "paper.pdf",
    # "doc_id": "sample1.txt",
    # "doc_id": "abc.srt",
    "mode": "short",
    "export": "pdf"
}

res = requests.post(url, json=payload)
print("Status Code:", res.status_code)
print("Raw Response Text:", res.text)  
print("Response JSON:", res.json())