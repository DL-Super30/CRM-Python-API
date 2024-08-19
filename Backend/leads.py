from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
from fastapi.openapi.docs import get_swagger_ui_html
from datetime import datetime
import logging


app = FastAPI(docs_url=None)

@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Skill-Capital API")

origins = ["http://localhost:3000",
           "http://127.0.0.1:3000"
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'jayanth'
DB_PORT = '5432'


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

class Lead(BaseModel):
    name: str
    cc : str
    phone : int
    email: str
    fee_quoted: int
    batch_timing: datetime
    description: str
    lead_status : str
    lead_source : str
    stack : str
    course : str
    class_mode : str
    next_followup : datetime

@app.post("/Insert Leads")
async def insert_lead(lead: Lead):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if not check_table_exists("public", "leads"):
            create_table_query = sql.SQL('''
                CREATE TABLE public.leads (
                    name VARCHAR(255),
                    cc VARCHAR(255),
                    phone INT,
                    email VARCHAR(255),
                    fee_quoted INT,
                    batch_timing TIMESTAMP,
                    description TEXT,
                    lead_status VARCHAR(50),
                    lead_source VARCHAR(50),
                    stack VARCHAR(50),
                    course VARCHAR(50),
                    class_mode VARCHAR(50),
                    next_followup TIMESTAMP
                );
            ''')
            cur.execute(create_table_query)
            conn.commit()

        insert_query = sql.SQL('''
            INSERT INTO public.leads (name, cc, phone, email, fee_quoted, batch_timing, description, lead_status, lead_source, stack, course, class_mode, next_followup)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
            ''')
        
        values = (
            lead.name, lead.cc , lead.phone , lead.email , lead.fee_quoted, lead.batch_timing, lead.description, lead.lead_status , lead.lead_source , lead.stack , lead.course , lead.class_mode , lead.next_followup
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




# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
        
#     except JWTError:
#         raise credentials_exception

# @app.get("/users")
# async def read_users_me(current_user: dict = Security(get_current_user)):
#     return {"user": current_user}