import os
from db import db
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from models.user import UserModel
from security import authenticate, identity  
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
db_host = os.getenv("DB_URL")
db_name = os.getenv("DB_NAME")
db_password = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'vibo'
api = Api(app)

jwt = JWTManager(app)  # No additional arguments

# **Set up JWT callbacks**
@jwt.user_identity_loader
def user_identity_lookup(user_id):
    return user_id  # This stores `user.id` in the JWT token as "sub"

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    return UserModel.find_by_id(jwt_data["sub"])  # Retrieve user object from token

# **Login endpoint**
@app.route('/auth', methods=['POST'])
def auth():
    from flask import request

    data = request.get_json()
    print("Auth request received:", data)  # Debugging

    user = authenticate(data['username'], data['password'])
    print("User found:", user)  # Debugging

    if not user:
        return jsonify({"message": "Invalid Credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


db.init_app(app)


if __name__ == '__main__':
    if app.config['DEBUG']:
        with app.app_context():      
            db.create_all()

    app.run(port=5000)