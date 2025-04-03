from unittest import TestCase
from app import app
from db import db
from sqlalchemy.sql import text
from dotenv import load_dotenv
import os

load_dotenv()
db_host = os.getenv("DB_URL")
db_name = os.getenv("DB_NAME")
db_password = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")

class BaseTest(TestCase):    
    @classmethod
    def setUpClass(cls):        
        cls.app = app  
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
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
        

    