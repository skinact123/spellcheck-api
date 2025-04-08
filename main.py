from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/spellcheck")
async def verify_token(token: str = ""):
    return JSONResponse(content={"status": "ok"})

@app.post("/spellcheck")
async def spellcheck(request: Request):
    body = await request.json()
    
    # Extract the message content
    message = body.get("message", "").lower()

    # Example spell check logic
    corrections = {
        "hellooo": "hello",
        "hiiiii": "hi",
        "byee": "bye",
        "chat": "chatbot"
    }

    corrected_message = corrections.get(message, message)

    # Only return the field that ChatBot accepts
    return {"fulfillmentText": f"Corrected: {corrected_message}"}
