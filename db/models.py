from pymongo import MongoClient
from bson.objectid import ObjectId 
import string, random


uri_web = ""
uri_local = "mongodb://localhost:27017"
client = MongoClient(uri_local)
db = client['CarbAPI']

Drivers = db["Drivers"]
Passengers = db["Passengers"]


class DriversDb:
    def __init__(self) -> None:
        self.collection = Drivers
        
    def create_user(self, user_dtls):
        return self.collection.insert_one(user_dtls).inserted_id
         
    def get_user_by_phone_num(self, phone_num):
        return self.collection.find_one({"_id": phone_num})
    
    def get_user_by_mail_addr(self, mail_addr):
        return self.collection.find_one({"mail_addr": mail_addr})
    
    def get_user_by_oid(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})
    
    def update_user_profile(self, user_id, dtls):
        return self.collection.update_one({"uid":user_id},{"$set":dtls.__dict__}).modified_count>0
    
    def update_user_role(self, user_id, dtls):
        return self.collection.update_one({"uid":user_id},{"$set":dtls}).modified_count>0
    
    def update_user_profile_by_oid(self, _id, dtls):
        return self.collection.update_one({"_id": ObjectId(_id)},{"$set":dtls.__dict__}).modified_count>0
    
    def delete_user(self, _id):
        return self.collection.delete_one({"_id":ObjectId(_id)}).deleted_count>0
    
    def get_all_users(self):
        return self.collection.find().sort("uid")
    
    def get_all_users_limited(self):
        return self.collection.find().limit(4)
    
    
        
class PassengersDb:
    def __init__(self) -> None:
        self.collection = Passengers
        
    def get_user_by_phone_num(self, phone_num):
        return self.collection.find_one({"phone_num": phone_num})
    
    def get_user_by_oid(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})
    
    def update_user_profile(self, user_id, dtls):
        return self.collection.update_one({"uid":user_id},{"$set":dtls.__dict__}).modified_count>0
    
    def update_user_role(self, user_id, dtls):
        return self.collection.update_one({"uid":user_id},{"$set":dtls}).modified_count>0
    
    def update_user_profile_by_oid(self, _id, dtls):
        return self.collection.update_one({"_id": ObjectId(_id)},{"$set":dtls.__dict__}).modified_count>0
    
    def delete_user(self, _id):
        return self.collection.delete_one({"_id":ObjectId(_id)}).deleted_count>0
    
    def get_all_users(self):
        return self.collection.find().sort("uid")
    

class Generate:
    def OTP():
            length = int(5)
            characters = string.digits
            otp = ""     
            for index in range(length):
                otp = otp + random.choice(characters)
                
            return otp