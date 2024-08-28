from fastapi import APIRouter
from pydantic import BaseModel
import bcrypt 
from prisma import Prisma
import logging
from fastapi import FastAPI, HTTPException, Depends
from app.auth.auth_handler import signJWT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

prisma = Prisma()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


class CreateClientDto(BaseModel):
    email: str
    name: str
    password: str
    
class UserLoginDto(BaseModel):
    email: str
    password: str
    
@router.post("/users")
def create_user(dto: CreateClientDto):
    try:
        password= bcrypt.hashpw(dto.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = prisma.user.create(
            data={
                "email": dto.email,
                "name": dto.name,
                "password": password
            }
        )
        return user
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.post("/login")
def login(dto: UserLoginDto):
    try:
        user = prisma.user.find_unique(where={"email": dto.email})
        if bcrypt.checkpw(dto.password.encode('utf-8'), user.password.encode('utf-8')):
            return signJWT(user.email)
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")