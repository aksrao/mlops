import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from google import genai
import json

load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("hugging_face_api")

if GOOGLE_API_KEY and HF_TOKEN:
    print("Check: Keys Loaded successfully.")
else:
    print("Check: Keys Missing! Check your `.env` file.")

# ********** Load the LLMs *****************

gemini_client = genai.Client(api_key=GOOGLE_API_KEY)
hf_client = InferenceClient(token=HF_TOKEN)
HF_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct" 

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
STORE_POLICY = """
RETURN POLICY:
1. Items can be returned within 30 days of purchase.
2. Electronics have a 15% restocking fee if opened.
3. Software subscriptions are non-refundable.
"""

def answer_with_context(user_query):

    # Constructing the system prompt with context
    system_instruction = f"""
        You are a support bot. Answer the user query using ONLY the policy below.

        ### POLICY DATA
        {STORE_POLICY}
        ###
    """
    full_prompt = f"{system_instruction}\nUser Query: {user_query}"

    return get_cloud_completion(full_prompt), get_oss_completion(user_query, system_instruction)


# query = "I opened the box for my laptop but want to return it. Is it free?"
# response1, response2 = answer_with_context(query)


# print(f"response from Gemini:", response1.text)
# print(f"Response from meta-llama:", response2.choices[0].message.content)

sys_msg = "You are a helpful assistant"
user_query = "You have to convert a word into a codified numeric string. For example, ABC will become 123; XYZ will become 242526. What will TUV be in this case?"
print(get_oss_completion(user_query, sys_msg).choices[0].message.content)