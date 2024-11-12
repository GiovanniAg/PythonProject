import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class EnvModel(BaseModel):
    app_name: str
    enviroment: str
    server_host: str
    server_port: int
    is_dev: bool
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str
    

env = EnvModel(
    app_name=os.getenv("APP_NAME", "ProductService"),
    enviroment=os.getenv("ENVIRONMENT", "dev"),
    server_host=os.getenv("SERVER_HOST", "0.0.0.0"),
    server_port=int(os.getenv("SERVER_PORT", "3000")),
    is_dev=os.getenv("ENVIRONMENT", "dev") == "dev",
    db_host=os.getenv("DATABASE_HOST"),
    db_port=os.getenv("DATABASE_PORT"), 
    db_name=os.getenv("DATABASE_NAME"),
    db_user=os.getenv("DATABASE_USER"),
    db_pass=os.getenv("DATABASE_PASSWORD")
)
