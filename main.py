from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
import logging
from pydantic import BaseModel
import bcrypt 
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Initialize Prisma client
prisma = Prisma()

app = FastAPI(
    title="service name",
    version="0.0.1",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/swagger.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateClientDto(BaseModel):
    email: str
    name: str
    password: str
    
class UserLoginDto(BaseModel):
    email: str
    password: str
    
class CreateLeadDto(BaseModel):
    name: str
    lead_source : str
    phone : int
    email: str
    lead_status : str
    
class CreateLeadDetailsDto(BaseModel):
    name: str
    cc : str
    phone : int
    email: str
    fee_quoted: int
    description: str
    lead_status : str
    lead_source : str
    stack : str
    course : str
    class_mode : str
    next_followup : str
    

    
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
                "name": dto.name,
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
        user = prisma.user.find_unique(where={"email": dto.email})
        if bcrypt.checkpw(dto.password.encode('utf-8'), user.password.encode('utf-8')):
            return signJWT(user.email)
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/my-details",dependencies=[Depends(JWTBearer())])
def get_my_details(token: str = Depends(JWTBearer())):
    try:
        user = prisma.user.find_unique(where={"email": token})
        return user
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
    
@app.post("/leads")
def create_lead(dto: CreateLeadDto):
    try:
        lead = prisma.lead.create(
            data={
                "name": dto.name,
                "lead_source": dto.lead_source if dto.lead_source else "website",
                "phone": dto.phone,
                "email": dto.email,
                "lead_status": dto.lead_status.values(),
            }
        )
        return lead
    except Exception as e:
        logging.error(f"Error creating lead: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/lead-details")
def create_lead_details(dto: CreateLeadDetailsDto):
    try:
        lead = prisma.lead.create(
            data={
                "name": dto.name,
                "cc": dto.cc,
                "phone": dto.phone,
                "email": dto.email,
                "fee_quoted": dto.fee_quoted,
                "description": dto.description,
                "lead_status": dto.lead_status,
                "lead_source": dto.lead_source,
                "stack": dto.stack,
                "course": dto.course,
                "class_mode": dto.class_mode,
                "next_followup": dto.next_followup
            }
        )
        return lead
    except Exception as e:
        logging.error(f"Error creating lead: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.get('/leads/count-per-hour')
def get_leads_count_per_hour():
    try:
        query = """
        SELECT EXTRACT(HOUR FROM "createdAt") AS hour, COUNT(*) AS count
        FROM "Lead"
        WHERE "createdAt"::date = CURRENT_DATE
        GROUP BY hour
        ORDER BY hour;
        """
        result =  prisma.query_raw(query)
        return {int(row['hour']): int(row['count']) for row in result}
    except Exception as e:
        logging.error(f"Error getting leads count per hour: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

