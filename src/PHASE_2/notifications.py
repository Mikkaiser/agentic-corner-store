import os
from datetime import datetime
import requests
from agents import function_tool

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
LOG_FILE = "owner_notifications.log"


def send_to_fallback(subject, text_body):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} | {subject} | {text_body}"
    print(f"[notify] {line}")
    with open(LOG_FILE, "a") as file:
        file.write(line + "\n")


def send_to_pushover(subject, text_body):
    payload = {
        "user": os.getenv("PUSHOVER_USER"),
        "token": os.getenv("PUSHOVER_TOKEN"),
        "title": subject,
        "message": text_body,
    }
    response = requests.post(PUSHOVER_URL, data=payload, timeout=10)
    response.raise_for_status()


def send_message(subject, text_body, html_body):
    try:
        send_to_pushover(subject, text_body)
        print("[notify] sent with pushover")
        return
    except Exception as error:
        print(f"[notify] pushover failed: {error}")
    print("[notify] using fallback")
    send_to_fallback(subject, text_body)


@function_tool
def notify_owner(subject: str, text_body: str, html_body: str) -> str:
    """
    Sends a notification to the store owner, for example when an order is placed
    or when a product is running low on stock.

    Args:
        subject: A short title for the notification
        text_body: The notification content as plain text
        html_body: The notification content as HTML
    """
    send_message(subject, text_body, html_body)
    return "Notification sent"
