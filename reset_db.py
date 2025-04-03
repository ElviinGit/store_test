from app import app
from db import db

with app.app_context():
    db.drop_all()  # Deletes all tables
    db.create_all()
    
    print("Database reset successfully!")
