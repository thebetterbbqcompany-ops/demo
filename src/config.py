import logging
import os

SECRET_KEY = "bazzite-locked-key"
ALGORITHM = "HS256"
DATABASE_URL = "grills.db"
TOKEN_EXPIRATION_HOURS = 24

# JORGE LOGGING STANDARD
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("better-bbq")

def log_system(msg: str):
    print(f"🖥️  [SYSTEM]   {msg}")

def log_ai(grill_id: str, thought: str):
    print(f"🧠 [AGENT:{grill_id[:4]}] {thought}")
