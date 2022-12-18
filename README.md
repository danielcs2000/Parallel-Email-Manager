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

![image](https://user-images.githubusercontent.com/34191864/208284243-ce5c571d-1fb8-4938-9252-c867946f9b73.png)


Executed emails per 0.5 seconds

![executed_emails](https://user-images.githubusercontent.com/34191864/208284279-5165bd83-7790-407a-b9e3-c00eaf6bbb29.jpeg)


Failed emails per 0.5 seconds


![failed_emails](https://user-images.githubusercontent.com/34191864/208284282-67fe1ad7-02cc-4c2d-988e-5994c866e882.jpeg)


New emails per 0.5 seconds added to the queue


![new_emails](https://user-images.githubusercontent.com/34191864/208284286-c5ab3a2d-4526-4af0-953b-9603ccececd2.jpeg)



Sent emails report (Full text in `reports/sent_emails.txt`)

Contains (id, attempts, priority) 

![image](https://user-images.githubusercontent.com/34191864/208284343-a41610d6-134f-4d03-a26d-4190160a867e.png)



