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

# ✅ Separate GET endpoint only for Chatbot.com webhook verification
@app.get("/verify")
async def verify_webhook(verification_token: str = ""):
    return Response(content=verification_token, media_type="text/plain")

# Optional root endpoint (for manual health check)
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

# POST endpoint for spellcheck
@app.post("/spellcheck")
async def spell_check(request: Request):
    data = await request.json()
    input_text = data.get("text", "")
    suggestions = sym_spell.lookup_compound(input_text, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else input_text
    return {"corrected": corrected}
