from agents import Agent, Runner, trace, function_tool, OpenAIChatCompletionsModel, output_guardrail, GuardrailFunctionOutput
import io
import re
import logging
import requests
from pypdf import PdfReader
logger = logging.getLogger(__name__)
@function_tool
def pdf_reader(link: str)->str:
    """
    Reads a PDF file from the given file path or URL and extracts all of its text content.
    
    Args:
        link (str): The local file path or web URL to the PDF document.
        
    Returns:
        str: The extracted text from all pages of the PDF.
    """
    logger.info(f"Reading PDF from {link}")
    try:
        if link.startswith("http"):
            # If it's a Google Drive link, we MUST convert it to a direct download link
            if "drive.google.com" in link:
                # Extract the file ID from URLs like .../file/d/<ID>/view...
                match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', link)
                if match:
                    file_id = match.group(1)
                    link = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            pdf_file = io.BytesIO(response.content)
            reader = PdfReader(pdf_file)
        else:
            reader = PdfReader(link)
            
        result = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                result += text
        logger.info(f"PDF read successfully: {link} and result is : {result} ")
        return result
    except Exception as e:
        return f"Failed to read PDF from {link}. Error: {str(e)}"

import requests
from bs4 import BeautifulSoup
import sqlite3
import os

@function_tool
def webscraper(url: str) -> str:
    """
    Scrapes the text content of a given URL. Useful for reading LinkedIn, GitHub, or portfolio sites.
    
    Args:
        url (str): The URL of the webpage to scrape.
        
    Returns:
        str: The extracted text content from the webpage.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

@function_tool
def dbreader(query: str) -> str:
    """
    Queries the internal vector database for information related to Ramveer.
    
    Args:
        query (str): The search query to look for in the database.
        
    Returns:
        str: The context found in the database, or an empty string if nothing matches.
    """
    db_url = os.getenv("LIBSQL_URL", "file:./local.db")
    db_path = db_url.replace("file:", "")
    
    # TODO: Implement vector embeddings generation (OpenAI) and LibSQL vector search here.
    # For MVP, we can return empty to force the agent to use the scraper/pdf reader tools first.
    return ""

@function_tool
def save_to_vector_db(text: str) -> str:
    """
    Saves newly scraped information into the vector database for future reference.
    
    Args:
        text (str): The text information to save.
        
    Returns:
        str: Success message.
    """
    # TODO: Implement vector embeddings generation and LibSQL INSERT here.
    return "Successfully saved to database."

@function_tool
def writetodb(email: str) -> str:
    """
    Saves a user's contact email to the database so Ramveer can contact them.
    
    Args:
        email (str): The user's email address.
        
    Returns:
        str: Success message.
    """
    try:
        from core.database import record_visitor_email
        success = record_visitor_email(email)
        if success:
            return "Contact information saved successfully to the visitors table. Ramveer will reach out soon!"
        else:
            return "Failed to save contact information to the database."
    except Exception as e:
        return f"Error saving contact info: {str(e)}"

tools = [pdf_reader, webscraper, dbreader, save_to_vector_db, writetodb]