from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from symspellpy.symspellpy import SymSpell, Verbosity
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace this with your actual token from Chatbot.com
CHATBOT_VERIFICATION_TOKEN = "abc123"

# Webhook verification endpoint for Chatbot.com
@app.get("/verify")
async def verify_webhook():
    return Response(content=CHATBOT_VERIFICATION_TOKEN, media_type="text/plain")

# Optional root endpoint
@app.get("/")
def root():
    return {"message": "Spellcheck API is running"}

# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dict_path = "frequency_dictionary_en_82_765.txt"

if os.path.exists(dict_path):
    sym_spell.load_dictionary(dict_path, term_index=0, count_index=1)
else:
    raise FileNotFoundError("Dictionary file not found")

# Spellcheck POST endpoint
@app.post("/spellcheck")
async def spell_check(request: Request):
    data = await request.json()
    input_text = data.get("text", "")
    suggestions = sym_spell.lookup_compound(input_text, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else input_text
    return {"corrected": corrected}
