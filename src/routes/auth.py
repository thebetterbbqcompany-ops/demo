from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from src.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_HOURS

router = APIRouter()

class AuthRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
def login(auth: AuthRequest):
    # 1. Log the Attempt
    print(f"🔐 AUTH ATTEMPT: User '{auth.username}'")

    # 2. Verify Credentials
    if auth.username == "admin" and auth.password == "password":
        token = jwt.encode({
            "sub": auth.username,
            "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS)
        }, SECRET_KEY, algorithm=ALGORITHM)
        
        # 3. Log Success
        print(f"✅ AUTH SUCCESS: Token Issued for '{auth.username}'")
        return {"access_token": token, "token_type": "bearer"}
    
    # 4. Log Failure
    print(f"🛑 AUTH FAILURE: Invalid Credentials for '{auth.username}'")
    raise HTTPException(status_code=401, detail="Incorrect credentials")
