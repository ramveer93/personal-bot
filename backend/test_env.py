from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)
val = os.getenv("ALLOWED_SCRAPE_DOMAINS")
print("RAW VALUE:", repr(val))
try:
    data = json.loads(val)
    print("JSON PARSED:", data)
except Exception as e:
    print("JSON ERROR:", repr(e))
