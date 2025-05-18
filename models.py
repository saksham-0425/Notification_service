from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Notification(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.String(50), nullable=False )
    type=db.Column(db.String(10), nullable=False)
    message=db.Column(db.Text, nullable=False)
    status=db.Column(db.String(20), default='pending')