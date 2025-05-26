# worker/consumer.py

import pika
import json
import time
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

from models import db, Notification
from app import app  # Ensure app is imported to initialize db

# Load SMTP credentials from .env
load_dotenv()
from_email = os.getenv("SMTP_EMAIL")
app_password = os.getenv("SMTP_PASS")


def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, app_password)
        server.sendmail(from_email, [to_email], msg.as_string())
        server.quit()
        print(f"📨 Email successfully sent to {to_email}")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        raise


def process_notification(data):
    fail_times = 2
    with app.app_context():  # Ensure DB operations have Flask context
        notif = Notification.query.get(data['notification_id'])
        if not notif:
            print(f"❌ Notification ID {data['notification_id']} not found.")
            return

        retries = 0
        max_retries = 3
        while retries < max_retries:
            try:
                print(f"📨 Sending {notif.type} to user {notif.user_id}")
                if retries < fail_times:
                    raise Exception("Simulated failure for testing retries")

                if notif.type == 'email':
                    send_email(
                        to_email=notif.user_id,
                        subject="BSS YUN HI",
                        body=notif.message
                    )

                time.sleep(1)  # Simulate sending delay
                notif.status = 'sent'
                db.session.commit()
                print(f"✅ Notification {notif.id} sent successfully.")
                break

            except Exception as e:
                retries += 1
                print(f"⚠️ Retry {retries} failed: {e}")
                time.sleep(1)

        if retries == max_retries:
            notif.status = 'failed'
            db.session.commit()
            print(f"❌ Notification {notif.id} failed after {max_retries} retries.")


def callback(ch, method, properties, body):
    print("📬 Received a message from queue.")
    data = json.loads(body)
    process_notification(data)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='notification_queue', durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='notification_queue', on_message_callback=callback)
        print("🚀 Worker is listening for notifications...")
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        print("❌ Failed to connect to RabbitMQ. Is the server running?")
        print(e)


if __name__ == '__main__':
    main()
