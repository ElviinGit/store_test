from models.user import UserModel
from tests.base_test import BaseTest
import json
from app import app

class UserTest(BaseTest):
    def test_register_user(self):
        with self.client as client:
                response = client.post('/register', json={'username': "elvin",
                                                         "password": 123})
                
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('elvin'))
                self.assertDictEqual({"message": "User created successfully"}, response.json)
            
           
    def test_register_and_login(self):
        with self.client as client:
                client.post("/register", json={"username": "test", "password": "1234"})
                auth_request = client.post("/auth",
                                           json={"username": "test", "password": "1234"},
                                           headers={'Content-Type': 'application/json'})
                
                self.assertIn('access_token', auth_request.get_json().keys())

              
    def test_register_duplicate_user(self):
        with self.client as client:
            client.post('/register', json={'username': "test", "password": 1234})
            response = client.post('/register', json={'username': "test", "password": 1234})
            
            self.assertEqual(response.status_code, 400)
            self.assertDictEqual({"message": "A user with that username already exists"}, response.json)
            