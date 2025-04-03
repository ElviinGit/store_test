from unittest import TestCase
from app import app
from db import db
from sqlalchemy.sql import text


class BaseTest(TestCase):    
    @classmethod
    def setUpClass(cls):        
        cls.app = app  
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:vibos1Sql@localhost:3306/mytestdatabase'
        cls.app.config['TESTING'] = True        
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
    
    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop() 
        
    def setUp(self):
        self.client = self.app.test_client()
        db.session.execute(text("TRUNCATE TABLE users"))
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        db.session.execute(text("TRUNCATE table items")) 
        db.session.execute(text("TRUNCATE TABLE stores"))
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.session.commit()# Force DELETE for MySQL
 
             
        with self.app_context:
            db.drop_all()
            db.create_all()
            
    def tearDown(self):
        with self.app_context:
            db.session.remove()
        

    