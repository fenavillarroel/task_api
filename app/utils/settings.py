import os
from dotenv import load_dotenv
load_dotenv()

USERNAME_DB = os.getenv('DB_USERNAME')
PASSWORD_DB = os.getenv('DB_PASSWORD')
DB_HOST = '127.0.0.1'
DB_PORT = 5432
DB_NAME = 'tasks'

SECRET_KEY: str = os.getenv('SECRET_KEY')
TOKEN_EXPIRE: int = 60

TASK_STATES = {
    0: 'Pending',
    1: 'Progress',
    2: 'Complete',
    3: 'Cancel'
}

page = 1
size_page = 10

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{USERNAME_DB}:{PASSWORD_DB}@{DB_HOST}:{DB_PORT}/{DB_NAME}'