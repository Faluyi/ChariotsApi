import os
from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from redis import Redis

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

app.secret_key = os.urandom(32)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'carb78154@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('CARB_API_EMAIL_APP_PWD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['CLOUD_KEY'] = os.environ.get('CLOUD_KEY')
app.config['CLOUD_SECRET'] = os.environ.get('CLOUD_SECRET')
app.config['DB_URI'] = os.environ.get('DB_URI')
app.config['DB_PWD'] = os.environ.get('DB_PWD')

app.config['REDIS_URL'] ="redis://localhost:6379/0"

mail = Mail(app)
redis = Redis.from_url(app.config['REDIS_URL'], decode_responses = True)


