from flask import jsonify
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from db.models import *
from config import *

Drivers_db = DriversDb()
Passengers_db = PassengersDb()

class SignUp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mail_addr', type=str, help='Email is required', required=True)
        parser.add_argument('pwd', type=str, help='Password is required', required=True)
        parser.add_argument('full_name', type=str, help='Full name is required', required=True)
        parser.add_argument('phone_num', type=int, help='Phone number is required', required=True)
        parser.add_argument('username', type=str, help='Username is required', required=True)
        parser.add_argument('addr', type=str, help='Residential address is required', required=True)        
        parser.add_argument('city', type=str, help='City is required', required=True)
        parser.add_argument('state', type=str, help='State is required', required=True)
        parser.add_argument('user_status', type=str, help='User status is required', required=True)
        
        args = parser.parse_args()
        
        user_dtls = {
            "mail_addr": args["mail_addr"],
            "pwd": generate_password_hash(args["pwd"]),
            "full_name": args["full_name"],
            "phone_num": args["phone_num"],
            "username": args["username"],
            "addr": args["addr"],
            "city": args["city"],
            "state": args["state"],
            "user_status": args["user_status"]
        }
        
        if args["user_status"] == "driver":
            try:
                user_id = Drivers_db.create_user(user_dtls)
                
                if user_id:
                    return jsonify({
                        "success": True,
                        "user_id": str(user_id)
                    }), 200
            except:
                return jsonify({
                    "success": False,
                    "message": "The phone number provided already exist in the database"
                })
        
        elif args["user_status"] == "passenger":
            user_id = Passengers_db.create_user(user_dtls)
            
            if user_id:
                return {
                    "success": True,
                    "user_id": user_id
                }, 200

        else:
            abort(400)


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone_num', type=int, help='Phone number is required', required=True)
        parser.add_argument('pwd', type=str, help='Password is required', required=True)
        parser.add_argument('user_status', type=str, help='User status is required', required=True)
        args = parser.parse_args()
        
        if args["user_status"] == "driver":
            driver = Drivers_db.get_user_by_phone_num(args["phone_num"])
            if driver:
                authenticated = check_password_hash(driver["pwd"], args["pwd"])
                if authenticated:
                    return {
                        "response": FormatResponse.driver(driver),
                        "success": True
                        }, 200
                else:
                    return {
                        "success": False, 
                        "message": "Invalid password"
                        }, 401
            else:
                return {
                        "success": False,
                        "message": "User does not exist"
                        }, 401
            
        elif args["user_status"] == "passenger":
            passenger = Passengers_db.get_user_by_phone_num(args["phone_num"])
            if passenger:
                authenticated = check_password_hash(driver["pwd"], args["pwd"])
                if authenticated:
                    return {
                        "response": passenger,
                        "success": True
                        }, 200
                else:
                    return {
                        "success": False,
                        "message": "Invalid password"
                        }, 401
            else:
                return {
                        "success": False,
                        "message": "User does not exist"
                        }, 401
            
        else:
            return {
                    "success": False,
                    "message": "Bad request"
                        }, 400
        
           
class AccountRecovery(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone_num', type=int, help='Phone_num is required', required=True)
        parser.add_argument('user_status', type=str, help='User status is required', required=True)
        args = parser.parse_args()
        
        if args["user_status"] == "driver":
            user_exist = Drivers_db.get_user_by_phone_num(args["phone_num"])
            
            if user_exist:
                otp = Generate.OTP()
                mail_addr = user_exist["mail_addr"]
                
                try:
                    msg = Message('Password Recovery', sender = 'carb@gmail.com', recipients = [mail_addr])
                    msg.body = f"Enter the OTP below into the requested field \nThe OTP will expire in 24 hours\n\nOTP: {otp}  \n\n\nFrom Carb"
                    
                    mail.send(msg)
                    
                    redis.set(args["phone_num"], otp, 86400)
                    return {
                        "success": True,
                        "message": "Mail sent"
                        }, 200
                    
                except:
                    return {
                        "success": False,
                        "message": "No internet connection"
                        }, 400
            else:
                return {
                        "success": False,
                        "message": "Invalid phone number"
                        }, 400
        
        elif args["user_status"] == "passenger":
            user_exist = Passengers_db.get_user_by_phone_num(args["phone_num"])
            
            if user_exist:
                otp = Generate.OTP()
                mail_addr = user_exist["mail_addr"]
                
                try:
                    msg = Message('Password Recovery', sender = 'carb@gmail.com', recipients = [mail_addr])
                    msg.body = f"Enter the OTP below into the requested field \nThe OTP will expire in 24 hours\n\nOTP: {otp}  \n\n\nFrom Carb"
                    
                    mail.send(msg)
                    redis.set(args["phone_num"], otp, 86400)
                    
                    return {
                        "success": True,
                        "message": "Mail sent"
                        }, 200
                    
                except:
                    return {
                        "success": False,
                        "message": "Bad request"
                        }, 400
            else:
                return {
                        "success": False,
                        "message": "User does not exist"
                        }, 401
            
        
        else:
            return {
                    "success": False,
                    "message": "Bad request"
                        }, 400


class PasswordReset(Resource):            
            
    def post(self, phone_num):
        parser = reqparse.RequestParser()
        parser.add_argument('otp', type=int, help='OTP is required', required=True)
        args = parser.parse_args()
        
        try:
            cached_otp = int(redis.get(phone_num))        
            app.logger.info(cached_otp)
            app.logger.info(args["otp"])
            
            if cached_otp:
                if int(args["otp"]) == int(cached_otp):
                    return {
                        "success": True,
                        "message": "Valid OTP" 
                    }, 200
            
                else:
                    return {
                        "success": False,
                        "message": "Invalid OTP"
                    }, 400
            else:
                return {
                    "success": False,
                    "message": "Resource not found"
                }, 404
        except:
            return {
                "success": False,
                "message": "Invalid phone address"
            }, 400
   
    def patch(self, phone_num):
        parser = reqparse.RequestParser()
        parser.add_argument('new_pwd', type=str, help='New password is required', required=True)
        args = parser.parse_args()
        
        dtls = {
            "pwd": generate_password_hash(args["new_pwd"])
        }
        updated = Drivers_db.update_user_profile(phone_num, dtls)
        
        if updated:
            return {
                "success": True,
                "message": "Password reset successful"
            }, 200
        
        else:
            return {
                "success": False,
                "message": "Password reset unsuccessful"
            }, 500
        


      
