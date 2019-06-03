#!/usr/bin/python3

import json
import requests
import time
from utils import url, session_token

def test_order_success():
    message = ["order", 12273, "KGI", "Sell", "Limit", "Day", 5, 1.245, 0]
    res = requests.post(
            url,
            data = json.dumps(message),
            headers={
                'session-token': session_token
                })
    #print(res)

    if res.status_code == 200:
        text = json.loads(res.text)
        print(text)
    
    time.sleep(100)

if __name__ == "__main__":
    test_order_success()


    
