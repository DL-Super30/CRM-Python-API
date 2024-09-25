from fastapi import FastAPI, HTTPException, Request, Depends, status, Security ,Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2 import Date, sql
from passlib.context import CryptContext
from fastapi.openapi.docs import get_swagger_ui_html
import uuid
from datetime import datetime, timedelta, timezone
import logging
from typing import List, Optional
from jose import JWTError, jwt
import secrets
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from datetime import time, date


SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3

app = FastAPI(docs_url=None)

@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Skill-Capital API")

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'jayanth'
DB_PORT = '5432'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

class Client(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    email: str

class OAuth2EmailPasswordRequestForm:
    def __init__(self, email: str = Form(...), password: str = Form(...)):
        self.email = email
        self.password = password

class Lead(BaseModel):
    name: str
    cc : str
    phone : str
    email: str
    fee_quoted: int
    batch_timing: str
    description: str
    lead_status : str
    lead_source : str
    stack : str
    course : str
    class_mode : str
    next_followup : datetime

class getLead(BaseModel):
    id: str
    name: str
    cc: str
    phone: str
    email: str
    fee_quoted: int
    batch_timing: str
    description: str
    lead_status: str
    lead_source: str
    stack: str
    course: str
    class_mode: str
    next_followup: datetime
    created_at: datetime

class Opportunity(BaseModel):
    name: str
    cc : str
    phone: str
    email: str
    fee_quoted: str
    batch_timing: str
    lead_status: str
    stack: str
    class_mode: str
    description: str
    oppo_status: str
    oppo_stage: str
    Demo_stage: str
    visited_stage: str
    lost_reason: str
    next_followup: datetime
    lead_source: str
    course: str

class getOpportunity(BaseModel):
    id:str
    name: str
    cc : str
    phone: str
    email: str
    fee_quoted: str
    batch_timing: str
    lead_status: str
    stack: str
    class_mode: str
    description: str
    oppo_status: str
    oppo_stage: str
    Demo_stage: str
    visited_stage: str
    lost_reason: str
    next_followup: datetime
    lead_source: str
    course: str
    created_at:datetime

class Learners(BaseModel):
    first_name : str
    id_proof : str
    DOB : datetime
    registered_date : str
    batch_id : str
    description : str
    source : str
    learner_owner : str
    currency : str
    counselling_done : str
    lastname : str
    phone : str
    email : str 
    location : str
    alternate_phone : str
    exchange_rate : str
    attended_demo : str
    learner_stage : str
    lead_createdtime : str

    registered_course : str
    tech_stack : str
    course_comments : str
    slack_access : str
    lms_access : str
    preferrable_time : str
    batch_timing : str
    class_mode : str
    comment : str

class getLearners(BaseModel):
    id : str
    first_name : str
    id_proof : str
    DOB : datetime
    registered_date : str
    batch_id : str
    description : str
    source : str
    learner_owner : str
    currency : str
    counselling_done : str
    lastname : str
    phone : str
    email : str 
    location : str
    alternate_phone : str
    exchange_rate : str
    attended_demo : str
    learner_stage : str
    lead_createdtime : str

    registered_course : str
    tech_stack : str
    course_comments : str
    slack_access : str
    lms_access : str
    preferrable_time : str
    batch_timing : str
    class_mode : str
    comment : str

class Batches(BaseModel):
    batch_name : str
    location : str
    slot : str
    trainer : str
    batch_status : str
    topic_status : str
    no_of_students : str
    learners : str
    stack : str
    start_time : datetime
    tentative_end_time : str
    class_mode : str
    stage : str
    comment : str

class getBatches(BaseModel):
    id : str
    batch_name : str
    location : str
    slot : str
    trainer : str
    batch_status : str
    topic_status : str
    no_of_students : str
    learners : str
    stack : str
    start_time : datetime
    tentative_end_time : str
    class_mode : str
    stage : str
    comment : str


class Months(BaseModel):
    date : date
    topic : str
    start_time : time
    end_time : time
    attendance : str
    vedio_upload : Optional[bool] = False
    duration : Optional[str] = ''

class getMonths(BaseModel):
    id : str
    date : date
    topic : str
    start_time : time
    end_time : time
    attendance : str
    vedio_upload : Optional[bool] = False
    duration : Optional[str] = None

class Trainers(BaseModel):
    trainer_name : str
    description : str
    id_proof : str
    trainer_status : str
    batches : str
    batch_stage : str
    trainer_owner : str
    free_slots : str
    tech_stack : str
    phone : str
    email : str
    location : str

class getTrainers(BaseModel):
    id : str
    trainer_name : str
    description : str
    id_proof : str
    trainer_status : str
    batches : str
    batch_stage : str
    trainer_owner : str
    free_slots : str
    tech_stack : str
    phone : str
    email : str
    location : str

# Any Table Existence
def check_table_exists(schema, table_name):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = sql.SQL(
            "SELECT EXISTS ("
            "SELECT FROM information_schema.tables "
            "WHERE table_schema = %s AND table_name = %s);"
        )
        
        cur.execute(query, (schema, table_name))
        exists = cur.fetchone()[0]
        cur.close()
        conn.close()
       
        return exists
    except (Exception, psycopg2.Error) as error:
        print(f"Error checking table existence: {error}")
        return False


#Inserting client.
@app.post("/insert_client/")
async def insert_client(client: Client):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if check_table_exists("public", "clients"):
            insert_query = sql.SQL('''
                INSERT INTO public.clients (id, email, password, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ''')
            
            client_id = str(uuid.uuid4())
            hashed_password = pwd_context.hash(client.password)
            created_at = updated_at = datetime.now(timezone.utc)
            insert_values = (client_id, client.email, hashed_password, created_at, updated_at)

            cur.execute(insert_query, insert_values)
            conn.commit()
            cur.close()
            conn.close()

            return {"message": f"Client {client.email} added successfully"}
            
        else:
            create_table_query = sql.SQL('''
                CREATE TABLE public.clients (
                    id UUID PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                );
                ALTER TABLE public.clients ADD CONSTRAINT email_non_empty CHECK (email <> '');
                ALTER TABLE public.clients ADD CONSTRAINT password_non_empty CHECK (password <> '');
            ''')

            cur.execute(create_table_query)
            conn.commit()

            client_id = str(uuid.uuid4())
            insert_query = sql.SQL('''
                INSERT INTO public.clients (id, email, password, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ''')

            hashed_password = pwd_context.hash(client.password)
            created_at = updated_at = datetime.now(timezone.utc)
            insert_values = (client_id, client.email, hashed_password, created_at, updated_at)

            cur.execute(insert_query, insert_values)
            conn.commit()
            cur.close()
            conn.close()

            return {"message": f"Client {client.email} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
# Access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#login authentication.
@app.post('/login', response_model=Token)
async def check_client(form_data: OAuth2EmailPasswordRequestForm = Depends()):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = sql.SQL('''
            SELECT password FROM public.clients WHERE email = %s
        ''')
        cur.execute(query, (form_data.email,))
        result = cur.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Client not found")

        stored_password = result[0]
        
        if not pwd_context.verify(form_data.password, stored_password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": form_data.email}, expires_delta=access_token_expires)

        cur.close()
        conn.close()

        return {"access_token": access_token, "token_type": "bearer", "email": form_data.email}

    except (Exception, psycopg2.Error) as e:
        raise HTTPException(status_code=500, detail=str(e))


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return {"email": email}
    except JWTError:
        raise credentials_exception


# Authorize clients
@app.get("/users")
async def read_users_me(current_user: dict = Security(get_current_user)):
    return {"user": current_user}



# Leads code
@app.post("/create_leads")
async def insert_lead(lead: Lead):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "leads"):
            create_table_query = sql.SQL('''
                CREATE TABLE public.leads (
                    id UUID PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    cc VARCHAR(255) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    fee_quoted INT NOT NULL,
                    batch_timing VARCHAR(50) NOT NULL,
                    description TEXT,
                    lead_status VARCHAR(50) NOT NULL,
                    lead_source VARCHAR(50) NOT NULL,
                    stack VARCHAR(50) NOT NULL,
                    course VARCHAR(50) NOT NULL,
                    class_mode VARCHAR(50) NOT NULL,
                    next_followup TIMESTAMP NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
            ''')
            cur.execute(create_table_query)
            conn.commit()

        insert_query = sql.SQL('''
            INSERT INTO public.leads (id, name, cc, phone, email, fee_quoted, batch_timing, description, lead_status, lead_source, stack, course, class_mode, next_followup, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)
            ''')
        client_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc)

        values = ( client_id,
            lead.name, lead.cc , lead.phone , lead.email , lead.fee_quoted, lead.batch_timing, lead.description, 
            lead.lead_status , lead.lead_source , lead.stack , lead.course , lead.class_mode , lead.next_followup,
            created_at
        )
    
        cur.execute(insert_query,values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Lead {lead.name} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Getting leads.
@app.get("/get_leads", response_model=List[getLead])
async def get_leads():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "leads"):
            raise HTTPException(status_code=404, detail=str('No data to display'))

        select_query = sql.SQL('''
            SELECT id, name, cc, phone, email, fee_quoted, batch_timing, description, lead_status, lead_source, stack, course, class_mode, next_followup, created_at
            FROM public.leads;
        ''')

        cur.execute(select_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        leads = []
        for row in rows:
            lead = getLead(
                id=row[0],
                name=row[1],
                cc=row[2],
                phone=row[3],
                email=row[4],
                fee_quoted=row[5],
                batch_timing=row[6],
                description=row[7],
                lead_status=row[8],
                lead_source=row[9],
                stack=row[10],
                course=row[11],
                class_mode=row[12],
                next_followup=row[13],
                created_at=row[14]
            )
            leads.append(lead)

        return leads

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#update lead
@app.put("/update_lead/{lead_id}")
async def update_lead(lead_id: str, lead: Lead):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "leads"):
            raise HTTPException(status_code=404, detail=str('No data to update'))
        
        query = sql.SQL('''
            SELECT id FROM public.leads WHERE id = %s
        ''')
        cur.execute(query, (lead_id,))
        existing_lead = cur.fetchone()

        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        update_query = sql.SQL('''
            UPDATE public.leads
            SET name = %s,
                cc = %s,
                phone = %s,
                email = %s,
                fee_quoted = %s,
                batch_timing = %s,
                description = %s,
                lead_status = %s,
                lead_source = %s,
                stack = %s,
                course = %s,
                class_mode = %s,
                next_followup = %s,
                created_at =%s
            WHERE id = %s
        ''')

        created_at = datetime.now(timezone.utc)

        updated_values = (
            lead.name, lead.cc, lead.phone, lead.email, lead.fee_quoted,
            lead.batch_timing, lead.description, lead.lead_status, lead.lead_source,
            lead.stack, lead.course, lead.class_mode, lead.next_followup, created_at, lead_id
        )

        cur.execute(update_query, updated_values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Lead {lead.name} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#Delete leads
@app.delete("/delete_lead/{lead_id}")
async def delete_lead(lead_id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "leads"):
            raise HTTPException(status_code=404, detail=str('No data to delete'))

        query = sql.SQL('''
            SELECT id,name FROM public.leads WHERE id = %s
        ''')
        cur.execute(query, (lead_id,))
        existing_lead = cur.fetchone()

        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        id , name = existing_lead

        delete_query = sql.SQL('''
            DELETE FROM public.leads WHERE id = %s
        ''')
        cur.execute(delete_query, (lead_id,))
        conn.commit()

        cur.close()
        conn.close()

        return {"message": f"Lead {name} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Opportunities
@app.post("/create_opportunity")
async def insert_opportunity(opportunity: Opportunity):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "opportunities"):
            create_table_query = sql.SQL('''
                CREATE TABLE public.opportunities (
                    id UUID PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    cc VARCHAR(255) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    fee_quoted VARCHAR(50) NOT NULL,
                    batch_timing VARCHAR(50) NOT NULL,
                    lead_status VARCHAR(50) NOT NULL,
                    stack VARCHAR(50) NOT NULL,
                    class_mode VARCHAR(50) NOT NULL,
                    description TEXT,
                    oppo_status VARCHAR(50) NOT NULL,
                    oppo_stage VARCHAR(50) NOT NULL,
                    Demo_stage VARCHAR(50) NOT NULL,
                    visited_stage VARCHAR(50) NOT NULL,
                    lost_reason VARCHAR(255),
                    next_followup TIMESTAMP NOT NULL,
                    lead_source VARCHAR(50) NOT NULL,
                    course VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
            ''')
            cur.execute(create_table_query)
            conn.commit()

        insert_query = sql.SQL('''
            INSERT INTO public.opportunities (id, name, cc, phone, email, fee_quoted, batch_timing, description, 
            lead_status, stack, class_mode, oppo_status, oppo_stage, Demo_stage, visited_stage, lost_reason, 
            next_followup, lead_source, course, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''')
        
        oppo_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc)

        values = (
            oppo_id, opportunity.name, opportunity.cc, opportunity.phone, opportunity.email, opportunity.fee_quoted, 
            opportunity.batch_timing, opportunity.description, opportunity.lead_status, opportunity.stack, 
            opportunity.class_mode, opportunity.oppo_status, opportunity.oppo_stage, opportunity.Demo_stage, 
            opportunity.visited_stage, opportunity.lost_reason, opportunity.next_followup, opportunity.lead_source, 
            opportunity.course, created_at
        )
    
        cur.execute(insert_query, values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Opportunity {opportunity.name} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# Getting Opportunities
@app.get("/get_Opportunities", response_model=List[getOpportunity])
async def get_opportunities():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "opportunities"):
            raise HTTPException(status_code=404, detail='No data to display')

        select_query = sql.SQL('''
            SELECT id, name, cc, phone, email, fee_quoted, batch_timing, description, 
                   lead_status, lead_source, stack, course, class_mode, oppo_status, oppo_stage, 
                   Demo_stage, visited_stage, lost_reason, next_followup, created_at
            FROM public.opportunities;
        ''')

        cur.execute(select_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        opportunities = []
        for row in rows:
            opportunity = getOpportunity(
                id=row[0],
                name=row[1],
                cc=row[2],
                phone=row[3],
                email=row[4],
                fee_quoted=row[5],
                batch_timing=row[6],
                description=row[7],
                lead_status=row[8],
                lead_source=row[9],
                stack=row[10],
                course=row[11],
                class_mode=row[12],
                oppo_status=row[13],
                oppo_stage=row[14],
                Demo_stage=row[15],
                visited_stage=row[16],
                lost_reason=row[17],
                next_followup=row[18],
                created_at=row[19]
            )
            opportunities.append(opportunity)

        return opportunities

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Update Opportunities
@app.put("/update_opportunity/{opportunity_id}")
async def update_opportunity(opportunity_id: str, opportunity: Opportunity):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "opportunities"):
            raise HTTPException(status_code=404, detail='No data to update')
        
        query = sql.SQL('''
            SELECT id FROM public.opportunities WHERE id = %s
        ''')
        cur.execute(query, (opportunity_id,))
        existing_opportunity = cur.fetchone()

        if not existing_opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found")

        update_query = sql.SQL('''
            UPDATE public.opportunities
            SET name = %s,
                cc = %s,
                phone = %s,
                email = %s,
                fee_quoted = %s,
                batch_timing = %s,
                description = %s,
                lead_status = %s,
                stack = %s,
                class_mode = %s,
                oppo_status = %s,
                oppo_stage = %s,
                Demo_stage = %s,
                visited_stage = %s,
                lost_reason = %s,
                next_followup = %s,
                lead_source = %s,
                course = %s,
                created_at = %s
            WHERE id = %s
        ''')

        created_at = datetime.now(timezone.utc)

        updated_values = (
            opportunity.name, opportunity.cc, opportunity.phone, opportunity.email, opportunity.fee_quoted,
            opportunity.batch_timing, opportunity.description, opportunity.lead_status, opportunity.stack,
            opportunity.class_mode, opportunity.oppo_status, opportunity.oppo_stage, opportunity.Demo_stage,
            opportunity.visited_stage, opportunity.lost_reason, opportunity.next_followup, opportunity.lead_source,
            opportunity.course, created_at, opportunity_id
        )

        cur.execute(update_query, updated_values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Opportunity {opportunity.name} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Delete Opportunities
@app.delete("/delete_opportunity/{opportunity_id}")
async def delete_opportunity(opportunity_id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "opportunities"):
            raise HTTPException(status_code=404, detail='No data to delete')

        query = sql.SQL('''
            SELECT id, name FROM public.opportunities WHERE id = %s
        ''')
        cur.execute(query, (opportunity_id,))
        existing_opportunity = cur.fetchone()

        if not existing_opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        
        oppo_id, name = existing_opportunity

        delete_query = sql.SQL('''
            DELETE FROM public.opportunities WHERE id = %s
        ''')
        cur.execute(delete_query, (oppo_id,))
        conn.commit()

        cur.close()
        conn.close()

        return {"message": f"Opportunity {name} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Learner
@app.post("/create_Leaners")
async def insert_learner(learner: Learners):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "learners"):
            create_table_query = sql.SQL('''
                CREATE TABLE public.learners (
                    id UUID PRIMARY KEY,
                    first_name VARCHAR(255) NOT NULL,
                    id_proof VARCHAR(255) NOT NULL,
                    DOB TIMESTAMP NOT NULL,
                    registered_date VARCHAR(50) NOT NULL,
                    batch_id VARCHAR(50) NOT NULL,
                    description TEXT,
                    source VARCHAR(50) NOT NULL,
                    learner_owner VARCHAR(50) NOT NULL,
                    currency VARCHAR(10) NOT NULL,
                    counselling_done VARCHAR(10) NOT NULL,
                    lastname VARCHAR(255) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    alternate_phone VARCHAR(20),
                    exchange_rate VARCHAR(10) NOT NULL,
                    attended_demo VARCHAR(10) NOT NULL,
                    learner_stage VARCHAR(50) NOT NULL,
                    lead_createdtime VARCHAR(50) NOT NULL,
                    registered_course VARCHAR(255) NOT NULL,
                    tech_stack VARCHAR(255) NOT NULL,
                    course_comments TEXT,
                    slack_access VARCHAR(10) NOT NULL,
                    lms_access VARCHAR(10) NOT NULL,
                    preferrable_time VARCHAR(50) NOT NULL,
                    batch_timing VARCHAR(50) NOT NULL,
                    class_mode VARCHAR(50) NOT NULL,
                    comment TEXT
                );
            ''')
            cur.execute(create_table_query)
            conn.commit()

        insert_query = sql.SQL('''
            INSERT INTO public.learners (
                id, first_name, id_proof, DOB, registered_date, batch_id, description, source,
                learner_owner, currency, counselling_done, lastname, phone, email, location,
                alternate_phone, exchange_rate, attended_demo, learner_stage, lead_createdtime,
                registered_course, tech_stack, course_comments, slack_access, lms_access,
                preferrable_time, batch_timing, class_mode, comment
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''')

        learner_id = str(uuid.uuid4())
        values = (
            learner_id, learner.first_name, learner.id_proof, learner.DOB, learner.registered_date, learner.batch_id,
            learner.description, learner.source, learner.learner_owner, learner.currency, learner.counselling_done,
            learner.lastname, learner.phone, learner.email, learner.location, learner.alternate_phone, learner.exchange_rate,
            learner.attended_demo, learner.learner_stage, learner.lead_createdtime, learner.registered_course, learner.tech_stack,
            learner.course_comments, learner.slack_access, learner.lms_access, learner.preferrable_time, learner.batch_timing,
            learner.class_mode, learner.comment
        )

        cur.execute(insert_query, values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Learner {learner.first_name} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Get Learners
@app.get("/get_learners", response_model=List[getLearners])
async def get_leaners():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "learners"):
            raise HTTPException(status_code=404, detail='No data to display')

        select_query = sql.SQL('''
            SELECT 
                id, first_name, id_proof, DOB, registered_date, batch_id, description, source,
                learner_owner, currency, counselling_done, lastname, phone, email, location,
                alternate_phone, exchange_rate, attended_demo, learner_stage, lead_createdtime,
                registered_course, tech_stack, course_comments, slack_access, lms_access,
                preferrable_time, batch_timing, class_mode, comment
            FROM public.learners;
        ''')

        cur.execute(select_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        learners = []
        for row in rows:
            learner = getLearners(
                id=row[0],
                first_name=row[1],
                id_proof=row[2],
                DOB=row[3],
                registered_date=row[4],
                batch_id=row[5],
                description=row[6],
                source=row[7],
                learner_owner=row[8],
                currency=row[9],
                counselling_done=row[10],
                lastname=row[11],
                phone=row[12],
                email=row[13],
                location=row[14],
                alternate_phone=row[15],
                exchange_rate=row[16],
                attended_demo=row[17],
                learner_stage=row[18],
                lead_createdtime=row[19],
                registered_course=row[20],
                tech_stack=row[21],
                course_comments=row[22],
                slack_access=row[23],
                lms_access=row[24],
                preferrable_time=row[25],
                batch_timing=row[26],
                class_mode=row[27],
                comment=row[28]
            )
            learners.append(learner)

        return learners

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Update Learner
@app.put("/update_learner/{learner_id}")
async def update_leaner(learner_id: str, learner: Learners):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "learners"):
            raise HTTPException(status_code=404, detail="No data to update")

        query = sql.SQL('''
            SELECT id FROM public.learners WHERE id = %s
        ''')
        cur.execute(query, (learner_id,))
        existing_learner = cur.fetchone()

        if not existing_learner:
            raise HTTPException(status_code=404, detail="Learner not found")

        update_query = sql.SQL('''
            UPDATE public.learners
            SET first_name = %s,
                id_proof = %s,
                DOB = %s,
                registered_date = %s,
                batch_id = %s,
                description = %s,
                source = %s,
                learner_owner = %s,
                currency = %s,
                counselling_done = %s,
                lastname = %s,
                phone = %s,
                email = %s,
                location = %s,
                alternate_phone = %s,
                exchange_rate = %s,
                attended_demo = %s,
                learner_stage = %s,
                lead_createdtime = %s,
                registered_course = %s,
                tech_stack = %s,
                course_comments = %s,
                slack_access = %s,
                lms_access = %s,
                preferrable_time = %s,
                batch_timing = %s,
                class_mode = %s,
                comment = %s
            WHERE id = %s
        ''')

        updated_values = (
            learner.first_name, learner.id_proof, learner.DOB, learner.registered_date, learner.batch_id, 
            learner.description, learner.source, learner.learner_owner, learner.currency, learner.counselling_done,
            learner.lastname, learner.phone, learner.email, learner.location, learner.alternate_phone,
            learner.exchange_rate, learner.attended_demo, learner.learner_stage, learner.lead_createdtime,
            learner.registered_course, learner.tech_stack, learner.course_comments, learner.slack_access,
            learner.lms_access, learner.preferrable_time, learner.batch_timing, learner.class_mode, learner.comment,
            learner_id
        )

        cur.execute(update_query, updated_values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Learner {learner.first_name} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Delete Learner
@app.delete("/delete_learner/{learner_id}")
async def delete_learner(learner_id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "learners"):
            raise HTTPException(status_code=404, detail="No data to delete")

        query = sql.SQL('''
            SELECT id, first_name FROM public.learners WHERE id = %s
        ''')
        cur.execute(query, (learner_id,))
        existing_learner = cur.fetchone()

        if not existing_learner:
            raise HTTPException(status_code=404, detail="Learner not found")

        id, first_name = existing_learner

        
        delete_query = sql.SQL('''
            DELETE FROM public.learners WHERE id = %s
        ''')
        cur.execute(delete_query, (learner_id,))
        conn.commit()

        cur.close()
        conn.close()

        return {"message": f"Learner {first_name} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Create batch
@app.post("/create_batch")
async def insert_batch(batch: Batches):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        
        if not check_table_exists("public", "batches"):
            create_table_query = sql.SQL('''
                CREATE TABLE public.batches (
                    id UUID PRIMARY KEY,
                    batch_name VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    slot VARCHAR(50) NOT NULL,
                    trainer VARCHAR(255) NOT NULL,
                    batch_status VARCHAR(50) NOT NULL,
                    topic_status VARCHAR(50) NOT NULL,
                    no_of_students VARCHAR(50) NOT NULL,
                    learners TEXT,
                    stack VARCHAR(50) NOT NULL,
                    start_time TIMESTAMP NOT NULL,
                    tentative_end_time VARCHAR(50) NOT NULL,
                    class_mode VARCHAR(50) NOT NULL,
                    stage VARCHAR(50) NOT NULL,
                    comment TEXT
                );
            ''')
            cur.execute(create_table_query)
            conn.commit()

        
        insert_query = sql.SQL('''
            INSERT INTO public.batches (id, batch_name, location, slot, trainer, batch_status, topic_status, no_of_students, learners, stack, start_time, tentative_end_time, class_mode, stage, comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''')

        batch_id = str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)

        values = (
            batch_id,batch.batch_name, batch.location, batch.slot, batch.trainer, batch.batch_status, 
            batch.topic_status, batch.no_of_students, batch.learners, batch.stack, batch.start_time, 
            batch.tentative_end_time, batch.class_mode, batch.stage, batch.comment
        )
        cur.execute(insert_query, values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Batch {batch.batch_name} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Batches
@app.get("/get_batches", response_model=List[getBatches])
async def get_batches():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the table exists
        if not check_table_exists("public", "batches"):
            raise HTTPException(status_code=404, detail="No batches available")

        # Fetch all batch details
        select_query = sql.SQL('''
            SELECT id, batch_name, location, slot, trainer, batch_status, topic_status, no_of_students, learners, stack, start_time, tentative_end_time, class_mode, stage, comment
            FROM public.batches;
        ''')

        cur.execute(select_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        batches = []
        for row in rows:
            batch = getBatches(
                id=row[0],
                batch_name=row[1],
                location=row[2],
                slot=row[3],
                trainer=row[4],
                batch_status=row[5],
                topic_status=row[6],
                no_of_students=row[7],
                learners=row[8],
                stack=row[9],
                start_time=row[10],
                tentative_end_time=row[11],
                class_mode=row[12],
                stage=row[13],
                comment=row[14]
            )
            batches.append(batch)

        return batches

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update batches
@app.put("/update_batch/{batch_id}")
async def update_batch(batch_id: str, batch: Batches):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "batches"):
            raise HTTPException(status_code=404, detail="No data to update")
        
        query = sql.SQL('''
            SELECT id FROM public.batches WHERE id = %s
        ''')
        cur.execute(query, (batch_id,))
        existing_batch = cur.fetchone()

        if not existing_batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        update_query = sql.SQL('''
            UPDATE public.batches
            SET batch_name = %s,
                location = %s,
                slot = %s,
                trainer = %s,
                batch_status = %s,
                topic_status = %s,
                no_of_students = %s,
                learners = %s,
                stack = %s,
                start_time = %s,
                tentative_end_time = %s,
                class_mode = %s,
                stage = %s,
                comment = %s
            WHERE id = %s
        ''')

        updated_values = (
            batch.batch_name, batch.location, batch.slot, batch.trainer,
            batch.batch_status, batch.topic_status, batch.no_of_students,
            batch.learners, batch.stack, batch.start_time, batch.tentative_end_time,
            batch.class_mode, batch.stage, batch.comment, batch_id
        )

        cur.execute(update_query, updated_values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Batch {batch.batch_name} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete batch
@app.delete("/delete_batch/{batch_id}")
async def delete_batch(batch_id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "batches"):
            raise HTTPException(status_code=404, detail="No data to delete")

        query = sql.SQL('''
            SELECT id, batch_name FROM public.batches WHERE id = %s
        ''')
        cur.execute(query, (batch_id,))
        existing_batch = cur.fetchone()

        if not existing_batch:
            raise HTTPException(status_code=404, detail="Batch not found with that ID")
        
        batch_id, batch_name = existing_batch

        delete_query = sql.SQL('''
            DELETE FROM public.batches WHERE id = %s
        ''')
        cur.execute(delete_query, (batch_id,))
        conn.commit()

        cur.close()
        conn.close()

        return {"message": f"Batch {batch_name} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create month
@app.post("/create_month")
async def insert_month(month: Months):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "months"):
            create_table_query = sql.SQL('''
                CREATE TABLE public.months (
                    id UUID PRIMARY KEY,
                    date TIMESTAMP NOT NULL,
                    topic VARCHAR(255) NOT NULL,
                    start_time TIME NOT NULL,
                    end_time TIME NOT NULL,
                    attendance VARCHAR(255) NOT NULL,
                    vedio_upload BOOLEAN DEFAULT FALSE,
                    duration VARCHAR(50)
                );
            ''')
            cur.execute(create_table_query)
            conn.commit()

        insert_query = sql.SQL('''
            INSERT INTO public.months (id, date, topic, start_time, end_time, attendance, vedio_upload, duration)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''')

        month_id = str(uuid.uuid4())

        values = (
            month_id, month.date, month.topic, month.start_time, month.end_time, 
            month.attendance, month.vedio_upload, month.duration
        )
        cur.execute(insert_query, values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Month entry for {month.topic} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Get Month
@app.get("/get_months", response_model=List[getMonths])
async def get_months():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "months"):
            raise HTTPException(status_code=404, detail="No months available")

        select_query = sql.SQL('''
            SELECT id, date, topic, start_time, end_time, attendance, vedio_upload, duration
            FROM public.months;
        ''')

        cur.execute(select_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        months = []
        for row in rows:
            month = getMonths(
                id=row[0],
                date=row[1].date(),
                topic=row[2],
                start_time=row[3],
                end_time=row[4],
                attendance=row[5],
                vedio_upload=row[6],
                duration=row[7]
            )
            months.append(month)

        return months

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update Month
@app.put("/update_month/{month_id}")
async def update_month(month_id: str, month: Months):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        check_query = sql.SQL('''
            SELECT * FROM public.months WHERE id = %s
        ''')
        cur.execute(check_query, (month_id,))
        existing_entry = cur.fetchone()

        if existing_entry is None:
            raise HTTPException(status_code=404, detail="Month entry not found")

        update_query = sql.SQL('''
            UPDATE public.months
            SET date = %s,
                topic = %s,
                start_time = %s,
                end_time = %s,
                attendance = %s,
                vedio_upload = %s,
                duration = %s
            WHERE id = %s
        ''')

        values = (
            month.date, month.topic, month.start_time, month.end_time,
            month.attendance, month.vedio_upload, month.duration, month_id
        )
        cur.execute(update_query, values)
        conn.commit()

        cur.close()
        conn.close()

        return {"message": f"Month entry {month.topic} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Delete month
@app.delete("/delete_month/{month_id}")
async def delete_month(month_id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        check_query = sql.SQL('''
            SELECT * FROM public.months WHERE id = %s
        ''')
        cur.execute(check_query, (month_id,))
        existing_entry = cur.fetchone()

        if existing_entry is None:
            raise HTTPException(status_code=404, detail="Month entry not found")

        delete_query = sql.SQL('''
            DELETE FROM public.months WHERE id = %s
        ''')
        cur.execute(delete_query, (month_id,))
        conn.commit()

        cur.close()
        conn.close()

        return {"message": f"Month entry deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Trainers
@app.post("/create_trainer")
async def insert_trainer(trainer: Trainers):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "trainers"):
            create_table_query = sql.SQL('''
                CREATE TABLE public.trainers (
                    id UUID PRIMARY KEY,
                    trainer_name VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
                    id_proof VARCHAR(255) NOT NULL,
                    trainer_status VARCHAR(50) NOT NULL,
                    batches VARCHAR(255) NOT NULL,
                    batch_stage VARCHAR(50) NOT NULL,
                    trainer_owner VARCHAR(255) NOT NULL,
                    free_slots VARCHAR(50) NOT NULL,
                    tech_stack VARCHAR(255) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NOT NULL
                );
            ''')
            cur.execute(create_table_query)
            conn.commit()

        insert_query = sql.SQL('''
            INSERT INTO public.trainers (id, trainer_name, description, id_proof, trainer_status, batches, batch_stage, trainer_owner, free_slots, tech_stack, phone, email, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''')

        trainer_id = str(uuid.uuid4())

        values = (
            trainer_id, trainer.trainer_name, trainer.description, trainer.id_proof, trainer.trainer_status, 
            trainer.batches, trainer.batch_stage, trainer.trainer_owner, trainer.free_slots, 
            trainer.tech_stack, trainer.phone, trainer.email, trainer.location
        )
        cur.execute(insert_query, values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Trainer {trainer.trainer_name} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get Trainers
@app.get("/get_trainers", response_model=List[getTrainers])
async def get_trainers():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "trainers"):
            raise HTTPException(status_code=404, detail="No trainers available")

        select_query = sql.SQL('''
            SELECT id, trainer_name, description, id_proof, trainer_status, batches, batch_stage, trainer_owner, free_slots, tech_stack, phone, email, location
            FROM public.trainers;
        ''')

        cur.execute(select_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        trainers = []
        for row in rows:
            trainer = getTrainers(
                id=row[0],
                trainer_name=row[1],
                description=row[2],
                id_proof=row[3],
                trainer_status=row[4],
                batches=row[5],
                batch_stage=row[6],
                trainer_owner=row[7],
                free_slots=row[8],
                tech_stack=row[9],
                phone=row[10],
                email=row[11],
                location=row[12]
            )
            trainers.append(trainer)

        return trainers

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Update trainer
@app.put("/update_trainer/{trainer_id}")
async def update_trainer(trainer_id: str, trainer: Trainers):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        check_query = sql.SQL('''
            SELECT * FROM public.trainers WHERE id = %s
        ''')
        cur.execute(check_query, (trainer_id,))
        existing_trainer = cur.fetchone()

        if existing_trainer is None:
            raise HTTPException(status_code=404, detail="Trainer not found")

        update_query = sql.SQL('''
            UPDATE public.trainers
            SET trainer_name = %s,
                description = %s,
                id_proof = %s,
                trainer_status = %s,
                batches = %s,
                batch_stage = %s,
                trainer_owner = %s,
                free_slots = %s,
                tech_stack = %s,
                phone = %s,
                email = %s,
                location = %s
            WHERE id = %s
        ''')

        values = (
            trainer.trainer_name, trainer.description, trainer.id_proof, trainer.trainer_status, trainer.batches, trainer.batch_stage, 
            trainer.trainer_owner, trainer.free_slots, trainer.tech_stack, trainer.phone, trainer.email, trainer.location, trainer_id
        )
        cur.execute(update_query, values)
        conn.commit()

        cur.close()
        conn.close()

        return {"message": f"Trainer {trainer.trainer_name} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete trainer 
@app.delete("/delete_trainer/{trainer_id}")
async def delete_trainer(trainer_id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        check_query = sql.SQL('''
            SELECT * FROM public.trainers WHERE id = %s
        ''')
        cur.execute(check_query, (trainer_id,))
        existing_trainer = cur.fetchone()

        if existing_trainer is None:
            raise HTTPException(status_code=404, detail="Trainer not found")

        delete_query = sql.SQL('''
            DELETE FROM public.trainers WHERE id = %s
        ''')
        cur.execute(delete_query, (trainer_id,))
        conn.commit()

        cur.close()
        conn.close()

        return {"message": f"Trainer deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
