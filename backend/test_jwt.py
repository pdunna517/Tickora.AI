from jose import jwt, JWTError
import base64
import json

SECRET_KEY = "YOUR_SUPER_SECRET_KEY_HERE_CHANGE_IN_PRODUCTION"
ALGORITHM = "HS256"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkB0aWNrb3JhLmNvbSIsImV4cCI6MTc3MTExNDA1NH0.eY-3bUJ_TX1nNEPc6W-ccQfVGMLgZwxD4QaOdIOsKP0"

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("Verification Successful!")
    print(payload)
except JWTError as e:
    print(f"Verification Failed: {e}")
except Exception as e:
    print(f"Error: {e}")
