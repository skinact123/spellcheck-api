from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from symspellpy.symspellpy import SymSpell, Verbosity
import os

app = FastAPI()

# Enable CORS for all origins (you can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SymSpell setup
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = "frequency_dictionary_en_82_765.txt"
if os.path.exists(dictionary_path):
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
else:
    raise FileNotFoundError("Dictionary file not found!")

# Webhook verification (GET request for platform setup)
@app.get("/spellcheck")
async def verify_webhook(challenge: str = "", token: str = ""):
    return Response(content=challenge, media_type="text/plain")

# Spellcheck endpoint (POST request during chat use)
@app.post("/spellcheck")
async def spellcheck(request: Request):
    data = await request.json()

    # 👇 Change this based on your chatbot's payload structure
    text = data.get("message", "")  # Chatbot.com sends "message"
    
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else text

    # 👇 This must return a FLAT dict with expected keys
    return {
        "fulfillmentText": corrected
    }
