# auth_service.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

app = FastAPI(title="JWT Authentication Service")

# ---------------- CONFIG ----------------
SECRET_KEY = "VERY_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Dummy users (DB simulation)
users_db = {
    "ajay": {
        "username": "ajay",
        "password_hash": pwd_context.hash("password123"),
        "role": "admin"
    },
    "user1": {
        "username": "user1",
        "password_hash": pwd_context.hash("userpass"),
        "role": "customer"
    }
}

# --------------- HELPERS -----------------
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or not verify_password(password, user["password_hash"]):
        return False
    return user

def create_access_token(data: dict, expires_minutes=30):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# --------------- LOGIN -------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return {"access_token": token, "token_type": "bearer"}


# --------------- VERIFY TOKEN ------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token")

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Token Expired or Invalid")


# --------------- PROTECTED ROUTES --------
@app.get("/secure")
def secure_area(user=Depends(get_current_user)):
    return {"message": "You accessed a protected API!", "user": user}


@app.get("/admin")
def admin_only(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {"message": "Welcome Admin!"}
