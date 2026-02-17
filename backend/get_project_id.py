import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("SQLALCHEMY_DATABASE_URI")
engine = create_engine(database_url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT id FROM projects LIMIT 1;")).fetchone()
    if result:
        print(f"PROJECT_ID={result[0]}")
    else:
        print("No projects found.")
