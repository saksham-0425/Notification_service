# Flask Notification Service with RabbitMQ

A simple Flask-based notification service that supports sending notifications via Email, SMS, and In-App messages. Notifications are queued using RabbitMQ and processed asynchronously by a worker (consumer.py).

---

## Features

- REST API to create and retrieve notifications
- Supports three notification types: `email`, `sms`, and `inapp`
- Uses RabbitMQ as a message broker for asynchronous processing
- Worker process listens to RabbitMQ queue and updates notification status
- Retry mechanism on notification delivery failure
- Uses SQLite database with SQLAlchemy ORM for persistence

## Project Structure

flask_assignment/
│
├── app.py # Flask app initialization and routes registration
├── models.py # SQLAlchemy models (Notification)
├── requirements.txt # Python dependencies
├── routes/
│ └── notifications.py # Notification API endpoints (Blueprint)
├── worker/
│ └── consumer.py # RabbitMQ worker that processes notifications
├── instance/ 
├ └── notifications.db   # SQLite database (auto-created)
└── templates/
  └── index.html # Home page template


---

## Getting Started

### Prerequisites

- Python 3.8+
- RabbitMQ Server ([Installation Guide](https://www.rabbitmq.com/download.html))
- `pip` for installing Python packages

### Installation

1. Clone the repo:
   ```bash
   git clone <https://github.com/saksham-0425/Notification_service>
   cd flask_assignment

