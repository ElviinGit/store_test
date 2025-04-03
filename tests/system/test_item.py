from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
from werkzeug.security import generate_password_hash
from db import db


class ItemTest(BaseTest):
    
    def set_up_auth(self):
        with self.app_context:  # Use parentheses to properly enter the context
            username = 'test'
            password = "1234"
            hashed_password = generate_password_hash(password) 

            # Check if the user already exists before creating a new one
            if not UserModel.find_by_username(username):
                user = UserModel(username, hashed_password)
                user.save_to_db()

            auth_request = self.client.post(
                '/auth',
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'}
            )

            auth_data = auth_request.get_json()
            auth_token = auth_data.get('access_token')

            if not auth_token:
                self.fail("Authentication failed. No access token received.")

            return {'Authorization': f'Bearer {auth_token}'}


    
    def test_item_no_auth(self):
        with self.client as client:
            resp = client.get('/item/test')
            self.assertEqual(resp.status_code, 401)
    
    def test_get_item_not_found(self):
        headers = self.set_up_auth()
        resp = self.client.get('/item/test', headers=headers)
        self.assertEqual(resp.status_code, 404)
        
    
    def test_get_item(self):
        headers = self.set_up_auth()
        StoreModel('test').save_to_db()
        ItemModel('test_item', 19.90, 1).save_to_db()
        resp = self.client.get('/item/test_item', headers=headers)
        self.assertEqual(resp.status_code, 200)
        
            
    def test_delete_item(self):
        headers = self.set_up_auth()
        StoreModel('test').save_to_db()
        ItemModel('test_item', 19.90, 1).save_to_db()
        resp = self.client.delete('/item/test_item', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual({"message": "Item deleted"}, resp.json)
        
                
    def test_create_item(self):
        StoreModel('test').save_to_db()
        resp = self.client.post('/item/test', json={'price': 15.15, 'store_id': 1})
        self.assertEqual(resp.status_code, 201)
        self.assertDictEqual({'name': 'test', 'price': 15.15}, resp.json)
        
    
    def test_duplicate_item(self):
        StoreModel('test').save_to_db()
        ItemModel('test_item', 15.15, 1).save_to_db()
        resp = self.client.post('/item/test_item', json={'price': 15.15, 'store_id': 1})
        self.assertEqual(resp.status_code, 400)
                
    def test_put_item(self):
        StoreModel('test').save_to_db()
        resp = self.client.put('/item/test', json={'price': 17.99, 'store_id': 1})
        self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
        self.assertDictEqual({'name': 'test', 'price': 17.99}, resp.json)
        
    def test_put_update_item(self):
        StoreModel('test').save_to_db()
        ItemModel('test_item', 15.14, 1).save_to_db()
        self.assertEqual(ItemModel.find_by_name('test_item').price, 15.14)
        resp = self.client.put('/item/test_item', json={'price': 17.99, 'store_id': 1})
        self.assertEqual(ItemModel.find_by_name('test_item').price, 17.99)
        self.assertDictEqual({'name': 'test_item', 'price': 17.99}, resp.json)
    
    def test_get_item_list(self):
        StoreModel('test').save_to_db()
        ItemModel('test', 15.14, 1).save_to_db()
        resp = self.client.get('/items')
        self.assertDictEqual({'items': [{'name': 'test', 'price': 15.14}]}, resp.json)
    
    
    
    
    
    
    