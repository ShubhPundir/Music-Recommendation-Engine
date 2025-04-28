import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# print(" COCKROACH_NAME:", os.getenv("COCKROACH_NAME"))
# print(" COCKROACH_USER:", os.getenv("COCKROACH_USER"))
# print(" COCKROACH_PASS:", os.getenv("COCKROACH_PASS"))
# print(" COCKROACH_HOST:", os.getenv("COCKROACH_HOST"))
# print(" COCKROACH_PORT:", os.getenv("COCKROACH_PORT"))


# Debug: Check if .env is loading correctly
print("🔍 COCKROACH_HOST from .env:", os.getenv("COCKROACH_HOST"))

def get_cockroach_connection():
    conn = psycopg2.connect(
        dbname="music",
        user=os.getenv("COCKROACH_USER"),
        password=os.getenv("COCKROACH_PASS"),
        host=os.getenv("COCKROACH_HOST"),
        port=os.getenv("COCKROACH_PORT"),
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
