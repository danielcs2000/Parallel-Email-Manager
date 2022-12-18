# Test 1

### Process to execute

Install dependencies with `python3 -m pip install -r requirements.txt`

Please run this script with `python3 index.py`

### Result images (based on 5 iterations)

#### Considerations

- If an email has **status pending**, **0 attempts** and **priority equal to 1**, then, it goes to the **pending queue**.
- If an email has **status pending**, **0 attempts** and **priority greater than 1**, then, it goes to the **priority queue**.
- If an email has **1 or more attempts**, then, it goes to the **retry queue**.


Executed emails per 0.5 seconds

![executed_emails](https://user-images.githubusercontent.com/34191864/208283386-140580e2-bf8f-4bbe-8fd6-cf1f85368394.jpeg)

Failed emails per 0.5 seconds

![failed_emails](https://user-images.githubusercontent.com/34191864/208283389-1447d6f1-8490-4f71-be9e-b9ae570f7f78.jpeg)

New emails per 0.5 seconds added to the queue

![new_emails](https://user-images.githubusercontent.com/34191864/208283390-96ab9e54-7931-47e7-bc19-01c4abaa7036.jpeg)

Sent emails report (id, attempts, priority)

![image](https://user-images.githubusercontent.com/34191864/208283403-bd2300ca-9d18-4ee9-9a15-166ca44dd863.png)
