import os
from dotenv import load_dotenv


load_dotenv()


GITHUB_API_URL = "https://api.github.com"
GITHUB_USER = os.getenv('GITHUB_USERNAME')
