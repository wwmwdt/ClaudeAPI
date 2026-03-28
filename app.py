import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

APP_NAME = "Claude API Wrapper"
APP_VERSION = "1.0.0"

app = FastAPI(title=APP_NAME, version=APP_VERSION)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"


class PromptRequest(BaseModel):
    message: str
    system: str = "You are a helpful assistant."


class PromptResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"app": APP_NAME, "version": APP_VERSION}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=PromptResponse)
async def ask(request: PromptRequest):
    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured")

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            ANTHROPIC_URL,
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "system": request.system,
                "messages": [{"role": "user", "content": request.message}],
            },
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    text = "".join(block["text"] for block in data["content"] if block["type"] == "text")
    return PromptResponse(response=text)
