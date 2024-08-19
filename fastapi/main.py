from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
import logging
from pydantic import BaseModel
import bcrypt 

# Initialize Prisma client
prisma = Prisma()

app = FastAPI(
    title="service name",
    version="0.0.1",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/swagger.json",
)

origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateClientDto(BaseModel):
    email: str
    fullname: str
    password: str
    
class UserLoginDto(BaseModel):
    email: str
    password: str
    
@app.on_event("startup")
def startup():
    logging.info("Connecting to the database...")
    prisma.connect()

@app.on_event("shutdown")
def shutdown():
    logging.info("Disconnecting from the database...")
    prisma.disconnect()

@app.post("/users")
def create_user(dto: CreateClientDto):
    try:
        password= bcrypt.hashpw(dto.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = prisma.user.create(
            data={
                "email": dto.email,
                "fullname": dto.fullname,
                "password": password
            }
        )
        return user
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.post("/login")
def login(dto: UserLoginDto):
    try:
        user = prisma.user.find_first(where={"email": dto.email})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not bcrypt.checkpw(dto.password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid password")
        return {
            "message": "Logged in successfully"
        }
    except Exception as e:
        logging.error(f"Error logging in: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

