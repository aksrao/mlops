import os
from typing import Union, List, Tuple, Optional
from dotenv import load_dotenv
import json
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from transformers import AutoTokenizer
from mongodb import insert_data
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from pymongo import MongoClient

load_dotenv(override=True)

app = FastAPI()

class parameters(BaseModel):
    model: Optional[str]
    SBU: str
    payload: Union[str, List[Tuple[str, str]]]
    temperature: Optional[float] = 1.0
    repo_id: Optional[str] = "deepseek-ai/DeepSeek-R1-0528"
    task: Optional[str] = "text-generation"
    provider: Optional[str] = "auto"

tokens_counter = Counter(
    "llm_tokens",
    "Total tokens used per SBU",
    ["sbu","model"]
)
tokens_input_counter = Counter(
    "llm_input_tokens",
    "total input tokens",
    ["sbu","model"]
)
tokens_output_counter = Counter(
    "llm_output_tokens",
    "total output tokens",
    ["sbu","model"]
)

def clean_markdown(text: str):
    return text.replace("\\n", "\n")

def record_tokens(provider, p: parameters,usage_metadata = None, output_text = None):
    log_data= {}
    if provider == "google":
        input_tokens = usage_metadata.get("input_tokens", 0)
        output_tokens = usage_metadata.get("output_tokens", 0)
        total_tokens = usage_metadata.get("total_tokens", input_tokens + output_tokens)
        
        log_data = {
            "sbu": p.SBU,
            "model": p.model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens
        }
        insert_data(log_data)
        print("Token usage recorded for", p.SBU)
    if provider == "Hugging_face":
        prompt = p.payload
        tokenizer = AutoTokenizer.from_pretrained(p.repo_id) 
        input_tokens = len(tokenizer.encode(prompt))
        output_tokens = len(tokenizer.encode(output_text))
        total_tokens = input_tokens + output_tokens
        log_data = {
            "sbu": p.SBU,
            "model": p.repo_id,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens
        }
        insert_data(log_data)
        print("Token usage recorded for", p.SBU)

@app.get("/gemini")
def gemini(p: parameters):
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    if GOOGLE_API_KEY:
        print("Check: Keys Loaded successfully.")
    else:
        print("Keys are missing")
    llm = ChatGoogleGenerativeAI(model=p.model, api_key=GOOGLE_API_KEY)
    messages=p.payload
    response= llm.invoke(messages)
    record_tokens("google",p ,usage_metadata=response.usage_metadata)
    return {"response": clean_markdown(response.text)}

@app.get("/hugging-face")
def hugging_face(p: parameters):

    HF_TOKEN = os.getenv("hugging_face_api")
    if HF_TOKEN:
        print("Check: Keys Loaded successfully.")
    else:
        print("hugging face tokens are missing")
    llm = HuggingFaceEndpoint(
        repo_id= p.repo_id,
        task= p.task,
        huggingfacehub_api_token=HF_TOKEN,
        temperature=p.temperature,
        provider=p.provider
    )
    chat = ChatHuggingFace(llm=llm)
    response = chat.invoke(p.payload)
    record_tokens("Hugging_face",p ,output_text=response.content)
    return {"response": clean_markdown(response.content)}

@app.get("/metrics")
def metrics():
    client = MongoClient("mongodb://localhost:27017")
    db = client["token_meter"]
    collection = db["data"]
    data = collection.aggregate([
        {
            "$group": {
                "_id": {
                    "sbu": "$sbu",
                    "model": "$model"
                },
                "total_tokens": {"$sum": "$total_tokens"},
                "output_tokens": {"$sum": "$output_tokens"},
                "input_tokens": {"$sum": "$input_tokens"}

            }
        }
    ])

    # Update Prometheus metrics
    for doc in data:
        sbu = doc["_id"]["sbu"]
        model = doc["_id"]["model"]
        input_tokens = doc["input_tokens"]
        output_tokens = doc["output_tokens"]
        total_tokens = doc["total_tokens"]
        tokens_counter.labels(sbu=sbu,model=model).inc(total_tokens)
        tokens_input_counter.labels(sbu=sbu,model=model).inc(input_tokens)
        tokens_output_counter.labels(sbu=sbu,model=model).inc(output_tokens)

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)