import random
import time
from enum import Enum
from multiprocessing import Process, Queue

from managers.info_manager import InfoManager
from models.generator.email import Email


class QueueState(Enum):
    PENDING = "pending"
    RETRY = "retry"
    PRIORITY = "priority"


class QueueInfo(Enum):
    SENT_EMAILS = "sent_emails"
    EXECUTED_EMAILS = "executed_emails"
    FAILED_EMAILS = "failed_emails"
    NEW_EMAILS = "new_emails"


class EmailQueueManager:
    __queue = []
    __queue_parallel = {
        QueueState.PENDING: Queue(),
        QueueState.PRIORITY: Queue(),
        QueueState.RETRY: Queue(),
    }
    __queue_sent_emails = Queue()

    __queue_info = {
        QueueInfo.SENT_EMAILS: Queue(),
        QueueInfo.EXECUTED_EMAILS: Queue(),
        QueueInfo.FAILED_EMAILS: Queue(),
        QueueInfo.NEW_EMAILS: Queue(),
    }

    __info_manager = InfoManager()

    # Script finishes aften n_sample iterations
    __n_sample = 5

    __n_subprocess = 8

    __enqueue_set = set()

    def __init__(self):
        # !!! You can't edit this section 11:14
        # This var "self.__queue" is the variable that save the current queue of emails
        self.__queue = self.__generate_emails(quantity=1)

        self.__queue_subprocess = {
            QueueState.PENDING: [Queue() for _ in range(self.__n_subprocess)],
            QueueState.RETRY: [Queue() for _ in range(self.__n_subprocess)],
            QueueState.PRIORITY: [Queue() for _ in range(self.__n_subprocess)],
        }

        self.__queue_process = {
            QueueState.PENDING: Process(
                target=self.__handle_queue_process, args=(QueueState.PENDING,)
            ),
            QueueState.RETRY: Process(
                target=self.__handle_queue_process, args=(QueueState.RETRY,)
            ),
            QueueState.PRIORITY: Process(
                target=self.__handle_queue_process, args=(QueueState.PRIORITY,)
            ),
        }

        self.__queue_parallel_processor()

    def __check_all_subprocess_empty_queues(self) -> bool:
        queues_empty = []
        for queue_state in QueueState:
            queues_empty.extend(
                [queue.empty() for queue in self.__queue_subprocess[queue_state]]
            )

        return all(queues_empty)

    def __check_all_process_empty_queues(self) -> bool:
        return all(
            [self.__queue_parallel[queue_state].empty() for queue_state in QueueState]
        )

    def __handle_subprocess(self, queue_state: QueueState, queue_idx: int) -> None:

        while True:

            if not self.__queue_subprocess[queue_state][queue_idx].empty():
                email = self.__queue_subprocess[queue_state][queue_idx].get()

                response = self.__send_email(email=email)
                response["timestamp"] = time.time()
                self.__queue_info[QueueInfo.EXECUTED_EMAILS].put(response)

                if response["status"] == "error":
                    self.__queue_subprocess[queue_state][queue_idx].put(
                        response["email"]
                    ) if queue_state == QueueState.RETRY else self.__queue_parallel[
                        QueueState.RETRY
                    ].put(
                        response["email"]
                    )
                    self.__queue_info[QueueInfo.FAILED_EMAILS].put(response)

                elif response["status"] == "sent":
                    self.__queue_sent_emails.put(response["email"])
                    self.__queue_info[QueueInfo.SENT_EMAILS].put(response)

            else:
                time.sleep(0.6) if queue_state == QueueState.RETRY else time.sleep(0.5)
                if not self.__check_all_subprocess_empty_queues():
                    continue
                time.sleep(1.1) if queue_state == QueueState.RETRY else time.sleep(0.5)
                if not self.__check_all_subprocess_empty_queues():
                    continue
                time.sleep(1.6) if queue_state == QueueState.RETRY else time.sleep(0.5)
                if not self.__check_all_subprocess_empty_queues():
                    continue
                time.sleep(2.1) if queue_state == QueueState.RETRY else time.sleep(0.5)
                if self.__check_all_subprocess_empty_queues():
                    return

    def __handle_queue_process(self, queue_state: QueueState) -> None:
        processes = [
            Process(target=self.__handle_subprocess, args=(queue_state, idx))
            for idx in range(self.__n_subprocess)
        ]
        [process.start() for process in processes]

        current_subprocess_idx = 0

        while True:

            if not self.__queue_parallel[queue_state].empty():
                email = self.__queue_parallel[queue_state].get()

                self.__queue_subprocess[queue_state][current_subprocess_idx].put(email)

                current_subprocess_idx += 1
                current_subprocess_idx %= self.__n_subprocess

            else:
                time.sleep(0.1)
                if not self.__check_all_process_empty_queues():
                    continue
                time.sleep(0.5)
                if not self.__check_all_process_empty_queues():
                    continue
                time.sleep(1)
                if self.__check_all_process_empty_queues():
                    break

        [process.join() for process in processes]

    def __queue_parallel_processor(self) -> None:

        [process.start() for process in self.__queue_process.values()]

        start = time.time()
        self.__info_manager.start_timestamp = start

        for _ in range(self.__n_sample):
            new_emails = self.__generate_emails(quantity=random.randint(1, 10))
            new_emails_info = {"value": len(new_emails), "timestamp": time.time()}
            self.__queue_info[QueueInfo.NEW_EMAILS].put(new_emails_info)

            self.__queue += new_emails

            self.__queue_sent_emails.put(None)
            sent_emails = list(iter(self.__queue_sent_emails.get, None))
            for sent_email in sent_emails:
                self.__enqueue_set.add(sent_email["id"])

            for idx, email in enumerate(self.__queue):

                if email["id"] in self.__enqueue_set:
                    del self.__queue[idx]
                    self.__enqueue_set.remove(email["id"])
                    continue

                if email["priority"] > 1:
                    self.__queue_parallel[QueueState.PRIORITY].put(email)
                    self.__enqueue_set.add(email["id"])

                elif email["status"] == "pending":
                    self.__queue_parallel[QueueState.PENDING].put(email)
                    self.__enqueue_set.add(email["id"])

            print(f"pending emails to send: {len(self.__queue)}")

            time.sleep(0.5)

        [process.join() for process in self.__queue_process.values()]

        assert self.__check_all_process_empty_queues()
        assert self.__check_all_subprocess_empty_queues()

        end = time.time()

        print(f"time elapsed: {end-start}")
        self.__generate_report()

    def __generate_report(self) -> None:

        self.__queue_info[QueueInfo.SENT_EMAILS].put(None)
        self.__info_manager.sent_emails = list(
            iter(self.__queue_info[QueueInfo.SENT_EMAILS].get, None)
        )

        self.__queue_info[QueueInfo.NEW_EMAILS].put(None)
        self.__info_manager.new_emails = list(
            iter(self.__queue_info[QueueInfo.NEW_EMAILS].get, None)
        )

        self.__queue_info[QueueInfo.EXECUTED_EMAILS].put(None)
        self.__info_manager.executed_emails = list(
            iter(self.__queue_info[QueueInfo.EXECUTED_EMAILS].get, None)
        )

        self.__queue_info[QueueInfo.FAILED_EMAILS].put(None)
        self.__info_manager.failed_emails = list(
            iter(self.__queue_info[QueueInfo.FAILED_EMAILS].get, None)
        )

        self.__info_manager.generate_overall_report()

    def __queue_processor(self):
        while True:
            self.__queue += self.__generate_emails(quantity=random.randint(1, 10))

            for idx, email in enumerate(self.__queue):
                if email["status"] == "sent":
                    del self.__queue[idx]
                    continue

                response = self.__send_email(email=email)

                self.__queue[idx] = response["email"]

            print(f"pending emails to send: {len(self.__queue)}")

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
                },
            },
        }

        print(
            f'[status:{response["email"]["status"]}] '
            + f'email:{response["email"]["id"]} '
            + f'attempts:{response["email"]["attempts"]} '
        )

        return response
