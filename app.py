from flask import Flask, render_template
from models import db
from routes.notifications import notifications_bp
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'

# Initialize database and register Blueprint
db.init_app(app)
app.register_blueprint(notifications_bp)

# Create DB tables if not exist
with app.app_context():
    db.create_all()

# Root route (optional: add basic HTML to templates/index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Entry point for both local dev and Render deployment
if __name__ == '__main__':
    # Bind to 0.0.0.0 and use PORT from env for Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
