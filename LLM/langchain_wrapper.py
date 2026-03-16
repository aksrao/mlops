import os
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


class Feedback(BaseModel):
    sentiment: Literal["positive", "neutral", "negative"]
    summary: str

load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("hugging_face_api")
OPEN_API_KEY = os.getenv("hf_open_ai")

if GOOGLE_API_KEY and HF_TOKEN and OPEN_API_KEY:
    print("Check: Keys Loaded successfully.")
else:
    print("Check: Keys Missing! Check your `.env` file.")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)
structured_model = llm.with_structured_output(
    schema=Feedback.model_json_schema(), method="json_schema"
)
messages = [
    (
        "system",
        "You are a Sentimental analysis AI agent. you will help to evaluate the senitiment of the user",
    ),
    ("human", "i like ice-cream"),
]
response = llm.invoke(messages)
# print(f"Sentiment:-",response.sentiment) # "positive"
print(response)
print(response.text.replace("**",""))
print(f"token usage:-", response.usage_metadata)

# ai_msg = llm.invoke(messages)
# print(ai_msg)
# print(ai_msg.text)