import sys
import os
from dotenv import load_dotenv

# Add backend to python path
sys.path.append(os.getcwd())

# Load environment variables
env_path = os.path.join(os.getcwd(), 'backend', '.env')
load_dotenv(env_path)

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_superuser(email, password):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User {email} already exists")
            return
        
        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            full_name="Super User",
            is_active=True,
            is_superuser=True
        )
        db.add(user)
        db.commit()
        print(f"Superuser {email} created successfully")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    import os
    # Add backend to python path
    sys.path.append(os.getcwd())
    
    email = input("Enter email: ")
    password = input("Enter password: ")
    create_superuser(email, password)
