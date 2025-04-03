from models.user import UserModel
from werkzeug.security import check_password_hash

def authenticate(username, password):
    '''
    Function That Gets Called When A User Calls The /auth Endpoint
    With Their Username And Password.
    :param username: User's username in string format.
    :param password: User's un-encrypted password in string format.
    :return: A UserModel if authentication was successful, None otherwise
    '''
    user = UserModel.find_by_username(username)
    if user and check_password_hash(user.password, password):
        return user
    return None

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)