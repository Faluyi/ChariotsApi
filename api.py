from db.models import *
from config import *
from resources.Api_resources import Login, SignUp, AccountRecovery, PasswordReset





        

api.add_resource(Login, '/user/login')
api.add_resource(SignUp, '/user/create')
api.add_resource(AccountRecovery, '/account/recover')
api.add_resource(PasswordReset, '/<int:phone_num>/password/reset')







if __name__ == "__main__":
    app.run(debug=True)