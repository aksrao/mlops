from fastapi import FastAPI
from google import genai
from fastapi.responses import StreamingResponse
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials
import os


app = FastAPI()

clerk_config = ClerkConfig(jwks_url=os.getenv("CLERK_JWKS_URL"))
clerk_guard = ClerkHTTPBearer(clerk_config)

@app.get("/api")
def idea(creds: HTTPAuthorizationCredentials = Depends(clerk_guard)):
    user_id = creds.decoded["sub"]
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    def event_stream():
        # Gemini streaming call
        stream = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents="Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"
        )

        for chunk in stream:
            if chunk.text:
                # SSE format
                for line in chunk.text.split("\n"):
                    yield f"data: {line}\n"
                yield "\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )                                       