from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

class TextResponse(BaseModel):
    text: List[str]

class FulfillmentMessage(BaseModel):
    text: TextResponse

class WebhookResponse(BaseModel):
    fulfillmentMessages: List[FulfillmentMessage]

@app.post("/spellcheck")
async def spellcheck(request: Request):
    data = await request.json()
    original_text = data.get("message", "Hello")
    
    # Correct the text here (placeholder logic)
    corrected = original_text.replace("hellooo", "hello").replace("hi", "Hello")

    response_data = WebhookResponse(
        fulfillmentMessages=[
            FulfillmentMessage(
                text=TextResponse(text=[f"Corrected: {corrected}"])
            )
        ]
    )
    
    return JSONResponse(content=response_data.dict())
