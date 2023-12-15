from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
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
            "pwd": args["pwd"],
            "full_name": args["full_name"],
            "_id": args["phone_num"],
            "username": args["username"],
            "addr": args["addr"],
            "city": args["city"],
            "state": args["state"],
            "user_status": args["user_status"]
        }
        
        if args["user_status"] == "driver":
            user_id = Drivers_db.create_user(user_dtls)
            
            if user_id:
                return {
                    "success": True,
                    "user_id": str(user_id)
                }, 200
        
        elif args["user_status"] == "passenger":
            user_id = Passengers_db.create_user(user_dtls)
            
            if user_id:
                return jsonify({
                    "success": True,
                    "user_id": user_id
                }), 200

        else:
            abort(400)


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone_num', type=str, help='Phone number is required', required=True)
        parser.add_argument('pwd', type=str, help='Password is required', required=True)
        parser.add_argument('user_status', type=str, help='User status is required', required=True)
        args = parser.parse_args()
        
        if args["user_status"] == "driver":
            driver = Drivers_db.get_user_by_phone_num(args["phone_num"])
            if driver:
                authenticated = check_password_hash(driver["pwd"], args["pwd"])
                if authenticated:
                    return {
                        "response": driver,
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
                        }
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
        parser.add_argument('mail_addr', type=str, help='Email is required', required=True)
        parser.add_argument('user_status', type=str, help='User status is required', required=True)
        args = parser.parse_args()
        
        if args["status"] == "driver":
            user_exist = Drivers_db.get_user_by_mail_addr(args["mail_addr"])
            
            if user_exist:
                otp = Generate.OTP()
                try:
                    msg = Message('Password Recovery', sender = 'carb@gmail.com', recipients = [args["mail_addr"]])
                    msg.body = f"Enter the OTP below into the requested field \nThe OTP will expire in 24 hours\n\nOTP: {otp}  \n\n\nFrom Carb"
                    
                    mail.send(msg)
                    return {
                        "success": True,
                        "message": "Mail sent"
                        }
                    
                except:
                    return {
                        "success": False,
                        "message": "Bad request"
                        }, 400
            else:
                return {
                        "success": False,
                        "message": "Invalid mail address"
                        }, 400
        
        elif args["status"] == "passenger":
            user_exist = Passengers_db.get_user_by_mail_addr(args["mail_addr"])
            
            if user_exist:
                otp = Generate.OTP()
                try:
                    msg = Message('Password Recovery', sender = 'carb@gmail.com', recipients = [args["mail_addr"]])
                    msg.body = f"Enter the OTP below into the requested field \nThe OTP will expire in 24 hours\n\nOTP: {otp}  \n\n\nFrom Carb"
                    
                    mail.send(msg)
                    return {
                        "success": True,
                        "message": "Mail sent"
                        }
                    
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
                
                
   
        
        


      
