import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
print(" DB_NAME:", os.getenv("DB_NAME"))
print(" DB_USER:", os.getenv("DB_USER"))
print(" DB_PASS:", os.getenv("DB_PASS"))
print(" DB_HOST:", os.getenv("DB_HOST"))
print(" DB_PORT:", os.getenv("DB_PORT"))


# Debug: Check if .env is loading correctly
print("🔍 DB_HOST from .env:", os.getenv("DB_HOST"))

def get_cockroach_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        sslmode='require'  # Required for CockroachDB Cloud
    )
    return conn

# Test the connection
if __name__ == "__main__":
    try:
        conn = get_cockroach_connection()
        print("✅ Connected to CockroachDB!")

        # Simple test query
        with conn.cursor() as cursor:
            cursor.execute("SELECT now();")
            current_time = cursor.fetchone()
            print("⏱️ Current Time from DB:", current_time[0])
        
        conn.close()
    except Exception as e:
        print("❌ Connection failed:")
        print(e)
