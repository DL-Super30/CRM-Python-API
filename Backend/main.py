from fastapi import FastAPI, HTTPException, Request, Depends, status, Security
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
from passlib.context import CryptContext
from fastapi.openapi.docs import get_swagger_ui_html
import uuid
from datetime import datetime, timedelta, timezone
import logging
from typing import List
# from jose import JWTError, jwt
# import secrets
# import os


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
    created_at : datetime

class getLead(BaseModel):
    name: str
    cc: str
    phone: str
    lead_status: str
    stack : str
    class_mode : str
    created_at : datetime

class getlead(BaseModel):
    id : str

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
            created_at = updated_at = datetime.utcnow()
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
            created_at = updated_at = datetime.utcnow()
            insert_values = (client_id, client.email, hashed_password, created_at, updated_at)

            cur.execute(insert_query, insert_values)
            conn.commit()
            cur.close()
            conn.close()

            return {"message": f"Client {client.email} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

#login authentication.
@app.post('/login')
async def check_client(client: Client):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        
        query = sql.SQL('''
            SELECT password FROM public.clients WHERE email = %s
        ''')
        cur.execute(query, (client.email,))
        result = cur.fetchone()

        
        if not result:
            raise HTTPException(status_code=404, detail="Client not found")

        stored_password = result[0]
        # print(stored_password)

        # print("Verifying password")
        if not pwd_context.verify(client.password, stored_password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        cur.close()
        conn.close()

        return {"message": f"Client {client.email} authenticated successfully"}

    except (Exception, psycopg2.Error) as e:
        # print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

#Leads code
@app.post("/createleads")
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

        return {"message": f"Client {lead.name} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        logging.error(f"Error checking table existence: {error}")
        return False


# Getting leads.
@app.get("/getleads", response_model=List[getLead])
async def get_leads():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "leads"):
            raise HTTPException(status_code=404, detail=str('No data to display'))

        select_query = sql.SQL('''
            SELECT name, cc, phone, lead_status, stack, class_mode, created_at
            FROM public.leads;
        ''')

        cur.execute(select_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        leads = []
        for row in rows:
            lead = getLead(
                name=row[0],
                cc=row[1],
                phone=row[2],
                lead_status=row[3],
                stack=row[4],
                class_mode=row[5],
                created_at=row[6]
            )
            leads.append(lead)

        return leads

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#Getting data for update lead. 
@app.get("/getlead_id/{lead_id}", response_model=getlead)
async def get_lead(lead_id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "leads"):
            raise HTTPException(status_code=404, detail=str('No data to display'))

        query = sql.SQL('''
            SELECT id FROM public.leads
            WHERE id = %s
        ''')
        cur.execute(query, (lead_id,))
        lead = cur.fetchone()

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        lead_data = {
            "id": lead[0]
        }

        cur.close()
        conn.close()

        return lead_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#update lead
@app.put("/updatelead/{lead_id}")
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
                created_at = %s
            WHERE id = %s
        ''')

        updated_values = (
            lead.name, lead.cc, lead.phone, lead.email, lead.fee_quoted,
            lead.batch_timing, lead.description, lead.lead_status, lead.lead_source,
            lead.stack, lead.course, lead.class_mode, lead.next_followup, lead.created_at, lead_id
        )

        cur.execute(update_query, updated_values)
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"Lead {lead.name} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#Delete leads
@app.delete("/deletelead/{lead_id}")
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
        id , name = existing_lead

        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead not found")

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
