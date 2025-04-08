from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

class UserRequest(BaseModel):
    message: str

@app.post("/spellcheck")
async def spellcheck(request: Request):
    data = await request.json()
    message = data.get("message", "")
    
    # ✅ Do your spell correction here:
    corrected_message = message.replace("hellooo", "hello")  # Example only

    # ✅ Return corrected response as `message`
    return {
        "message": corrected_message
    }

# Optional: for local testing only
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=10000)
