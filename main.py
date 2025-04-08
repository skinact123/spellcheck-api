from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/spellcheck")
async def spellcheck(request: Request):
    data = await request.json()

    user_message = data.get("message", "")
    corrected_message = correct_spelling(user_message)  # your spellchecker logic

    return JSONResponse(content={
        "fulfillmentText": corrected_message
    })

def correct_spelling(text):
    # Replace this with your actual logic
    return text.replace("hellooo", "hello").replace("hii", "hi")
