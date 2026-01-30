from fastapi import FastAPI
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()


@app.get("/")
def instant():
    GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")
    client = genai.Client(api_key=GEMINI_API_KEY)
    message = "You are on a website that has just been deployed to production for the first time! Please reply with an enthusiastic announcement to welcome visitors to the site, explaining that it is live on production for the first time!"
    response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents = message
    )
    reply = response.text.replace("\n", "<br/>") 
    html = f"<html><head><title>Live in an Instant!</title></head><body><p>{reply}</p></body></html>"
    return html