import io
import re
import requests
from pypdf import PdfReader

def pdf_reader_raw(link: str)->str:
    try:
        if link.startswith("http"):
            if "drive.google.com" in link:
                match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', link)
                if match:
                    file_id = match.group(1)
                    link = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            print(f"Downloading from: {link}")
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            print("Content type:", response.headers.get("Content-Type"))
            pdf_file = io.BytesIO(response.content)
            reader = PdfReader(pdf_file)
        else:
            reader = PdfReader(link)
            
        result = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                result += text
        return result
    except Exception as e:
        return f"Failed to read PDF from {link}. Error: {str(e)}"

url = "https://drive.google.com/file/d/15qsPqGNmtLwkeoGPK2_KwCJcJVOcYGFe/view?usp=sharing"
print(pdf_reader_raw(url)[:500])
