from tools.tools import pdf_reader

# The google drive URL from the .env file
url = "https://drive.google.com/file/d/15qsPqGNmtLwkeoGPK2_KwCJcJVOcYGFe/view?usp=sharing"
print("Testing pdf_reader...")
result = pdf_reader(url)
print(f"Result length: {len(result)}")
if "Failed to read" in result:
    print(f"ERROR: {result}")
else:
    print(f"First 200 chars: {result[:200]}")
