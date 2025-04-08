from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from symspellpy.symspellpy import SymSpell, Verbosity
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Verification route for chatbot.com Webhook
@app.get("/verify")
async def verify_webhook(verification_token: str = ""):
    # Chatbot expects this format: { "response": "your_token" }
    return JSONResponse(content={"response": verification_token})

# Optional root endpoint for checking status
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

# POST endpoint to correct spelling
@app.post("/spellcheck")
async def spell_check(request: Request):
    data = await request.json()
    input_text = data.get("text", "")
    suggestions = sym_spell.lookup_compound(input_text, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else input_text
    return {"corrected": corrected}
