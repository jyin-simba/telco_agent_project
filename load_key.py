from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()  # Looks for .env automatically

# Access variables
api_key = os.getenv("OPENAI_API_KEY")
telco_path = os.getenv("TELCO_DB_PATH")

print(f"API Key (partial): {api_key[:4]}...")
print(f"Telco DB path: {telco_path}")
