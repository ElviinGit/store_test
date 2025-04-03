from app import app
from db import db

with app.app_context():
    db.drop_all()  # Deletes all tables
    
    print("Database reset successfully!")
