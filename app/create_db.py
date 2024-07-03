from app import create_app, db
import os

app = create_app()

with app.app_context():
    print("Creating the database...")
    db.create_all()
    database_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite3')
    if os.path.exists(database_path):
        print("Database created successfully at:", database_path)
    else:
        print("Database creation failed!")
