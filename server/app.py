#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


users = [
    {'id': 1, 'username': 'user1', 'password': 'password1'},
    {'id': 2, 'username': 'user2', 'password': 'password2'},
 
]

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')  
        
        # Find the user by username (assuming usernames are unique)
        user = next((user for user in users if user['username'] == username), None)
        
        if user and user['password'] == password:  # Check if the password matches
            # Set the session's user_id value to user's id
            session['user_id'] = user['id']
            return jsonify(user), 200  # Return user data as JSON with 200 status
        
        return {'message': 'Invalid username or password'}, 401  # Return 401 for unauthorized

        
        
api.add_resource(Login, '/login')
    
class Logout(Resource):
    def delete(self):
        # Remove the user_id value from the session
        session.pop('user_id', None)
        return {}, 204

api.add_resource(Logout, '/logout')

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            # Return the user data as JSON with a 200 status code
            user = next((user for user in users if user['id'] == user_id), None)
            if user:
                return jsonify(user), 200
        return {}, 401  # Return 401 for unauthorized

api.add_resource(CheckSession, '/check_session')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
