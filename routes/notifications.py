from flask import Blueprint, request, jsonify
from models import db, Notification
import pika
import json

# ✅ Correctly create a Blueprint object
notifications_bp = Blueprint('notifications', __name__)

def publish_to_queue(notification_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notification_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='notification_queue',
        body=json.dumps(notification_data),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()



@notifications_bp.route('/notifications', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_id = data.get('user_id')
    notif_type = data.get('type')
    message = data.get('message')
    
    if notif_type not in ['email', 'sms', 'inapp']:
        return jsonify({'error': 'Invalid notification type'}), 400
    
    # ✅ Correct assignment (use '=' not '-')
    notification = Notification(user_id=user_id, type=notif_type, message=message, status='pending')
    db.session.add(notification)
    db.session.commit()

    publish_to_queue({
        'notification_id': notification.id,
        'user_id': user_id,
        'type': notif_type,
        'message': message
    })

    return jsonify({'message': f'{notif_type} notification queued for user {user_id}'}), 202

@notifications_bp.route('/users/<user_id>/notifications', methods=['GET'])
def get_user_notifications(user_id):
    # ✅ Correct model name (singular: Notification)
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([
        {'id': n.id, 'type': n.type, 'message': n.message, 'status': n.status}
        for n in notifications
    ])
