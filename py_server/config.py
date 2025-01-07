import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Server constants loaded from .env
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))
LOG_FILE = os.getenv('LOG_FILE')
DEBUG = os.getenv('DEBUG').lower()
env_file_path = os.getenv('linuxpath')
env_reread_on_query = os.getenv('REREAD_ON_QUERY').lower()
