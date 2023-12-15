from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from db.models import *
from config import *
from resources.Api_resources import *

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'carb@gmail.com'
app.config['MAIL_PASSWORD'] = email_pswd
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)



        

api.add_resource(Login, '/login')
api.add_resource(SignUp, '/user/create')
api.add_resource(AccountRecovery, '/account/recover')







if __name__ == "__main__":
    app.run(debug=True)