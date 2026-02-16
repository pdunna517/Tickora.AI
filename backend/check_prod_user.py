import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

def check_user(db_url, email):
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        # Using raw SQL to avoid model dependency issues if any
        result = db.execute(text("SELECT email FROM users WHERE email = :email"), {"email": email}).fetchone()
        if result:
            print(f"User {email} FOUND in database.")
        else:
            print(f"User {email} NOT FOUND in database.")
            
            # List all users
            all_users = db.execute(text("SELECT email FROM users")).fetchall()
            print(f"Total users: {len(all_users)}")
            for u in all_users:
                print(f" - {u[0]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL")
    email = "admin@tickora.com"
    if not db_url:
        print("DATABASE_URL not set")
    else:
        check_user(db_url, email)
