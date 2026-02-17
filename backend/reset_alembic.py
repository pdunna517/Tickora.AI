import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("SQLALCHEMY_DATABASE_URI")
if not database_url:
    print("SQLALCHEMY_DATABASE_URI not found")
    exit(1)

engine = create_engine(database_url)

with engine.connect() as conn:
    print("Resetting alembic_version to be16c0685dff...")
    conn.execute(text("DELETE FROM alembic_version;"))
    conn.execute(text("INSERT INTO alembic_version (version_num) VALUES ('be16c0685dff');"))
    conn.commit()
    print("Done.")
