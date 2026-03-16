import os
from dotenv import load_dotenv
import json
from google import genai
from huggingface_hub import InferenceClient

load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("hugging_face_api")

if GOOGLE_API_KEY and HF_TOKEN:
    print("Check: Keys Loaded successfully.")
else:
    print("Check: Keys Missing! Check your `.env` file.")

gemini_client = genai.Client(api_key=GOOGLE_API_KEY)

# Let's define a function to send the prompt to the LLM and fetch the response

def get_cloud_completion(prompt, model_id="gemini-2.5-flash"):      # Arguments: prompt and model
    """
    Sends a prompt to the Google Gemini API and returns the text response.
    """

    # Google Gemini uses the method <client.models.generate_content> to generate responses
    # This method varies across different providers

    response = gemini_client.models.generate_content(
                                                    model=model_id,
                                                    contents=prompt)
    return response

hf_client = InferenceClient(token=HF_TOKEN)

HF_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"        # Select a model from available ones on HuggingFace, you can choose any other model as well

def get_oss_completion(user_input, sys_msg = "You are a helpful technical assistant."):
    """
    Sends a message to Llama 3 via Hugging Face Inference API.
    """

    # Constructing the message payload
    messages = [
        {"role": "system", "content": sys_msg},        # Think of this as a system configuration prompt
        {"role": "user", "content": user_input}        # This is the placeholder for user's prompt or query
    ]


    # HF uses the <clinet.chat_completion> method
    response = hf_client.chat_completion(
                                        model=HF_MODEL,
                                        messages=messages,)

    return response
simple_query = "Explain the concept of 'latency' in software engineering in one sentence."
response = get_oss_completion(simple_query)
print(response)