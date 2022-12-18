import math

import matplotlib.pyplot as plt
import numpy as np


class InfoManager:
    def __init__(self) -> None:
        self.sent_emails = []
        self.executed_emails = []
        self.failed_emails = []
        self.new_emails = []
        self.start_timestamp = 0.0
        self.output_filepath = "reports/"

    def __generate_executed_emails_graph(self) -> None:
        self.executed_emails.sort(key=lambda x: x["timestamp"])
        observation_time = [
            email["timestamp"] - self.start_timestamp for email in self.executed_emails
        ]
        observation_time.sort()
        max_time = observation_time[-1]
        steps = math.ceil(max_time / 0.5) * 0.5

        x = 0.25 + np.arange(stop=steps, step=0.5)
        y = []
        for value in x:
            y.append(
                sum(
                    time_elapsed > value - 0.25 and time_elapsed <= value + 0.5
                    for time_elapsed in observation_time
                )
            )

        plt.bar(x, y, width=0.5, edgecolor="white", linewidth=1)
        plt.xlim([0, x[-1] + 0.25])
        plt.xticks(np.arange(stop=x[-1] + 0.5, step=0.5))
        plt.title("Number of emails executed per 0.5 seconds")
        plt.savefig(f"{self.output_filepath}executed_emails.jpeg")
        plt.clf()

    def __generate_failed_emails_graph(self) -> None:
        self.failed_emails.sort(key=lambda x: x["timestamp"])
        observation_time = [
            email["timestamp"] - self.start_timestamp for email in self.failed_emails
        ]
        observation_time.sort()
        max_time = observation_time[-1]
        steps = math.ceil(max_time / 0.5) * 0.5

        x = 0.25 + np.arange(stop=steps, step=0.5)
        y = []
        for value in x:
            y.append(
                sum(
                    time_elapsed > value - 0.25 and time_elapsed <= value + 0.5
                    for time_elapsed in observation_time
                )
            )

        plt.bar(x, y, width=0.5, edgecolor="white", linewidth=1)
        plt.xlim([0, x[-1] + 0.25])
        plt.xticks(np.arange(stop=x[-1] + 0.5, step=0.5))
        plt.title("Number of failed emails per 0.5 seconds")
        plt.savefig(f"{self.output_filepath}failed_emails.jpeg")
        plt.clf()

    def __generate_new_emails_graph(self) -> None:
        self.new_emails.sort(key=lambda x: x["timestamp"])

        observation_time = [
            email["timestamp"] - self.start_timestamp for email in self.new_emails
        ]
        max_time = observation_time[-1]
        steps = math.ceil(max_time / 0.5) * 0.5

        x = 0.25 + np.arange(stop=steps, step=0.5)
        y = [email["value"] for email in self.new_emails]

        plt.bar(x, y, width=0.5, edgecolor="white", linewidth=1)
        plt.xlim([0, x[-1] + 0.25])
        plt.xticks(np.arange(stop=x[-1] + 0.5, step=0.5))
        plt.title("Number of new emails added to the queue per 0.5 seconds")
        plt.savefig(f"{self.output_filepath}new_emails.jpeg")

        plt.clf()

    def __generate_sent_emails_report(self) -> None:
        with open(f"{self.output_filepath}sent_emails.txt", "w") as f:
            for email in self.sent_emails:
                email_id = email["email"]["id"]
                attemps = email["email"]["attempts"]
                priority = False if email["email"]["priority"] == 1 else True
                f.write(f"{email_id},{attemps},{priority}\n")

    def generate_overall_report(self) -> None:
        self.__generate_sent_emails_report()
        self.__generate_new_emails_graph()
        self.__generate_failed_emails_graph()
        self.__generate_executed_emails_graph()
