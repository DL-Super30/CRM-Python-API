from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
import logging
from pydantic import BaseModel
from app.auth.auth_bearer import JWTBearer
from datetime import datetime
from app.routers.users import users

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

app.include_router(
    users.router, 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
@app.on_event("startup")
def startup():
    logging.info("Connecting to the database...")
    prisma.connect()

@app.on_event("shutdown")
def shutdown():
    logging.info("Disconnecting from the database...")
    prisma.disconnect()


    
# class CreateLeadDto(BaseModel):
#     name: str
#     lead_source : str
#     phone : int
#     email: str
#     lead_status : str
    
class CreateLeadDetailsDto(BaseModel):
    name: str
    cc : str
    phone : int
    email: str
    feeQuoted: int
    batchTiming: str
    description: str
    leadStatus : str
    leadSource : str
    stack : str
    course : str
    classMode : str
    nextFollowUp : datetime
    




    

    
@app.get("/my-details",dependencies=[Depends(JWTBearer())])
def get_my_details(token: str = Depends(JWTBearer())):
    try:
        user = prisma.user.find_unique(where={"email": token})
        return user
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# @app.post("/leads")
# def create_lead(dto: CreateLeadDto):
#     try:
#         lead = prisma.lead.create(
#             data={
#                 "name": dto.name,
#                 "lead_source": dto.lead_source if dto.lead_source else "website",
#                 "phone": dto.phone, 
#                 "email": dto.email,
#                 "lead_status": dto.lead_status.values(),
#             }
#         )
#         return lead
#     except Exception as e:
#         logging.error(f"Error creating lead: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/lead-details")
def create_lead_details(dto: CreateLeadDetailsDto):
    try:
        lead_details = prisma.leaddetails.create(
            data={
                "name": dto.name,
                "cc": dto.cc,
                "phone": dto.phone,
                "email": dto.email,
                "feeQuoted": dto.feeQuoted,
                "batchTiming": dto.batchTiming,
                "description": dto.description,
                "leadStatus": dto.leadStatus,
                "leadSource": dto.leadSource,
                "stack": dto.stack,
                "course": dto.course,
                "classMode": dto.classMode,
                "nextFollowUp": dto.nextFollowUp
            }
        )
        return lead_details
    except Exception as e:
        logging.error(f"Error creating lead details: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/lead-details")
def get_lead_details():
    try:
        lead_details = prisma.leaddetails.find_many()
        return lead_details
    except Exception as e:
        logging.error(f"Error retrieving all lead details: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.put("/lead-details/{id}")
def update_lead_details(id: int, dto):
    try:
        lead_details = prisma.leaddetails.update(
            where={"id": id},
            data={
                "name": dto.name,
                "cc": dto.cc,
                "phone": dto.phone,
                "email": dto.email,
                "feeQuoted": dto.feeQuoted,
                "batchTiming": dto.batchTiming,
                "description": dto.description,
                "leadStatus": dto.leadStatus,
                "leadSource": dto.leadSource,
                "stack": dto.stack,
                "course": dto.course,
                "classMode": dto.classMode,
                "nextFollowUp": dto.nextFollowUp
            }
        )
        return lead_details
    except Exception as e:
       logging.error(f"Error updating lead details: {e}")
       raise HTTPException(status_code=500, detail="Internal Server Error")
   
@app.delete("/lead-details/{id}")
def delete_lead_details(id: int):
    try:
        lead_details = prisma.leaddetails.delete(where={"id": id})
        return lead_details
    except Exception as e:
        logging.error(f"Error deleting lead details: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
    
   






# @app.get('/leads_details/count-per-hour')
# def get_leads_count_per_hour():
#     try:
#         query = """
#         SELECT EXTRACT(HOUR FROM "createdAt") AS hour, COUNT(*) AS count
#         FROM "Lead"
#         WHERE "createdAt"::date = CURRENT_DATE
#         GROUP BY hour
#         ORDER BY hour;
#         """
#         result =  prisma.query_raw(query)
#         return {int(row['hour']): int(row['count']) for row in result}
#     except Exception as e:
#         logging.error(f"Error getting leads count per hour: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

