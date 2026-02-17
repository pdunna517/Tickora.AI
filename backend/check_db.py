import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("SQLALCHEMY_DATABASE_URI")
engine = create_engine(database_url)
inspector = inspect(engine)

print("Tables found:", inspector.get_table_names())
