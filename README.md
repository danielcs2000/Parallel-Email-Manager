# Test 1

### Process to execute

Install dependencies with `python3 -m pip install -r requirements.txt`

Please run this script with `python3 index.py`

### Result images (based on 20 iterations)

#### Considerations

- If an email has **status pending**, **0 attempts** and **priority equal to 1**, then, it goes to the **pending queue**.
- If an email has **status pending**, **0 attempts** and **priority greater than 1**, then, it goes to the **priority queue**.
- If an email has **1 or more attempts**, then, it goes to the **retry queue**.

Time elapsed 

![image](https://user-images.githubusercontent.com/34191864/208284559-1a839095-0b5e-45c3-a531-e6114dda4e41.png)


Executed emails per 0.5 seconds

![executed_emails](https://user-images.githubusercontent.com/34191864/208284564-9bf7f3b7-c036-4999-afb5-0bffcc15cda2.jpeg)


Failed emails per 0.5 seconds

![failed_emails](https://user-images.githubusercontent.com/34191864/208284569-8703bc5f-1b8e-4ad1-9baf-946b5b21e425.jpeg)


New emails per 0.5 seconds added to the queue

![new_emails](https://user-images.githubusercontent.com/34191864/208284574-065c73e9-4a02-4a3d-9f6a-63a87b2ec85a.jpeg)



Sent emails report (Full text in `reports/sent_emails.txt`)

Contains (id, attempts, priority) 

![image](https://user-images.githubusercontent.com/34191864/208284588-a95f5e9a-8c23-43c7-bdac-55a21b05e5c2.png)



