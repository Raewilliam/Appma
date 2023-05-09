import sys
import os
from dotenv import load_dotenv
from app import app as application

# Load environment variables
load_dotenv()

# Add the app directory to the system path
sys.path.insert(0, os.path.dirname(__file__))

# Set the environment variables for Flask
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_APP'] = 'app'

# Initialize the application
application.secret_key = os.getenv('FLASK_SECRET_KEY')
