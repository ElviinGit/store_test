from models.store import StoreModel
from tests.base_test import BaseTest
from models.item import ItemModel

class StoreTest(BaseTest):
    
    def test_create_store(self):
        with self.client as client:
            response = client.post('/store/test')
            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(StoreModel.find_by_name('test'))
            self.assertDictEqual({'name': 'test', 'items': []}, response.json)
    
    def test_create_duplicate_store(self):
        with self.client as client:
            client.post('/store/test')
            response = client.post('/store/test')
            self.assertDictEqual({'message': "A store with name 'test' already exists."}, response.json)
            self.assertEqual(response.status_code, 400)
    
    def test_delete_store(self):
        with self.client as client:
            StoreModel('test').save_to_db()
            
            resp = client.delete('/store/test')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual({'message': "Store deleted"}, resp.json)
            
    
    def test_find_sotre(self):
        with self.client as client:
            StoreModel('test').save_to_db()
            resp = client.get('store/test')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual({'name': 'test', 'items': []}, resp.json)
    
    def test_store_not_found(self):
        with self.client as client:
            response = client.get("store/test")
            self.assertEqual(response.status_code, 404)
    
    def test_store_found_with_item(self):
        with self.client as client:
            StoreModel('test').save_to_db()
            ItemModel('test_item', 19.99, 1).save_to_db()
            resp = client.get("store/test")
            self.assertDictEqual({'name': 'test', 'items': [{'name': 'test_item', 'price': 19.99}]}, resp.json)
    
    def test_store_list(self):
        with self.client as client:
            StoreModel('test').save_to_db()
            resp = client.get('/stores')
            self.assertDictEqual({'stores': [{'name': 'test', 'items': []}]}, resp.json)
            
  
    def test_store_list_with_item(self):
        with self.client as client:
            StoreModel('test').save_to_db()
            ItemModel('test_item', 19.99, 1).save_to_db()
            resp = client.get('/stores')
            self.assertDictEqual({'stores': [{'name': 'test', 'items': [{'name': 'test_item', 'price': 19.99}]}]}, resp.json)


            
            

    
    
    
    
    
        
        