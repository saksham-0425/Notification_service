from flask import Flask, render_template
from models import db
from routes.notifications import notifications_bp


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///notifications.db'

db.init_app(app)
app.register_blueprint(notifications_bp)

with app.app_context():
    db.create_all()
    
@app.route('/')
def home():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)



# if __name__=='__main__':
#     app.run(debug=True)