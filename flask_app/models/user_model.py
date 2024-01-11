from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    # TODO: Put In The Database Schema
    db = ""

    # Initializing the Users data in the database based off given information in the form
    def __init__(self, data):
        self.id = data['id']
        self.user_name = data['user_name']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # ______CLASS METHODS_______ #

    # methos for saving a single new user to database based off of HTML form
    @classmethod
    def save_new_user(cls, data):
        # The query variable that will be sent to the database
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                """
        # return statement to connect to the database
        return connectToMySQL(cls.db).query_db(query, data)

    # method for getting the info for one user by their ID
    @classmethod
    def get_one_user_by_id(cls, id):
        # query to get info from the database
        query = """
                SELECT * FROM users
                WHERE id = %(id)s
                """
        # results being saved into variable
        results = connectToMySQL(cls.db).query_db(query, id)
        # if statement to check if their is a user with that info in the database
        if not results:
            return False
        # if the user info is there, the info is stored into a user variable to be used
        user = cls(results[0])
        return user

    @classmethod
    def get_one_user_by_email(cls, data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # ______STATIC METHODS______ #

    # Validating user info when trying to log in or sign up
    @staticmethod
    def validate_user(data):
        # variable to set the boolean value
        is_valid = True
        # variable holding the database query
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                """
        # results from the database being stored into a variable
        results = connectToMySQL(User.db).query_db(query, data)
        # ______Validation Process______ #
        # checking to see if that email is already used in the database
        if len(results) >= 1:
            flash("Email already in use.", 'register')
            is_valid = False
        if len(data['first_name']) < 2:
            flash("First Name must be more then 3 characters", 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name must be more then 3 characters", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email", 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password needs 8 characters", 'register')
            is_valid = False
        if data['confirm_password'] != data['password']:
            flash("Passwords must match", 'register')
            is_valid = False

        return is_valid