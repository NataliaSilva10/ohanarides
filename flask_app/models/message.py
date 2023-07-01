from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user
from flask_app.models import ride
db = "ohana_rideshares"

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.ride_id = data['ride_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = None

    @classmethod
    def get_messages(cls,data):
        query = """
                SELECT * FROM messages 
                LEFT JOIN users as sender
                ON messages.sender_id = sender.id
                """
                # WHERE ride_id = %(ride_id)s;
        result = connectToMySQL(db).query_db(query,data)
        messages = []
        for row in result:
            this_message = cls(row)
            sender_data = {
                "id" : row["sender_id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["sender.created_at"],
                "updated_at" : row["sender.updated_at"],
            }
            this_message.sender = user.User(sender_data)
            messages.append(this_message)
        return messages

    @classmethod
    def save(cls,data):
        query = """
                INSERT INTO messages
                (ride_id,sender_id,content)
                VALUES (%(ride_id)s,%(sender_id)s,%(content)s);
                """
        connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data["content"]) < 2:
            flash("Message content must contain at least two characters", "message")
            is_valid = False
        return is_valid