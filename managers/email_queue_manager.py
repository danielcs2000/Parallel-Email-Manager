import time
import random

from models.generator.email import Email


class EmailQueueManager:
    __queue = []

    def __init__(self):
        # !!! You can't edit this section 11:14
        # This var "self.__queue" is the variable that save the current queue of emails
        self.__queue = self.__generate_emails(
            quantity=10
        )

        self.__queue_processor()

    def __queue_processor(self):
        while True:
            self.__queue += self.__generate_emails(
                quantity=random.randint(1, 10)
            )

            for idx, email in enumerate(self.__queue):
                if email["status"] == "sent":
                    del self.__queue[idx]
                    continue

                response = self.__send_email(
                    email=email
                )

                self.__queue[idx] = response["email"]

            print(f'pending emails to send: {len(self.__queue)}')

            time.sleep(0.5)

    # !!! You can't edit this method
    # This method generate an array with many emails that you should send after.
    def __generate_emails(self, quantity):
        return Email().generate_many(quantity=quantity)

    # !!! You can't edit this method
    # This method is used to send fake email, this method could delay from 0 to 1 second by every send process.
    def __send_email(self, email):
        time.sleep(random.uniform(0, 1))

        error = random.randint(0, 1)

        if error == 1:
            email["attempts"] += 1

        response = {
            "status": "sent" if error == 0 else "error",
            "email": {
                **email,
                **{
                    "status": "pending" if error == 1 else "sent",
                }
            },
        }

        print(
            f'[status:{response["email"]["status"]}] ' +
            f'email:{response["email"]["id"]} ' +
            f'attempts:{response["email"]["attempts"]} '
        )

        return response
