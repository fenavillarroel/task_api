import os
from dotenv import load_dotenv
load_dotenv()

username_db = os.getenv('DB_USERNAME')
password_db = os.getenv('DB_PASSWORD')
db_host = 'localhost'
db_port = 3306

secret_key: str = os.getenv('SECRET_KEY')
token_expire: int = 60

task_states = {
    0: 'Pending',
    1: 'Progress',
    2: 'Complete',
    3: 'Cancel'
}

page = 1
limit_page = 10
