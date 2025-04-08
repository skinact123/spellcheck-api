from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from symspellpy.symspellpy import SymSpell, Verbosity
import os

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Webhook verification (GET)
@app.get("/verify")
async def verify_webhook(challenge: str = "", token: str = ""):
    return Response(content=challenge, media_type="text/plain")

# Health check
@app.get("/")
def root():
    return {"message": "Spellcheck API is running"}

# Load dictionary
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dict_path = "frequency_dictionary_en_82_765.txt"
if os.path.exists(dict_path):
    sym_spell.load_dictionary(dict_path, term_index=0, count_index=1)
else:
    raise FileNotFoundError("Dictionary file not found")

# ✅ Actual POST webhook (spellcheck)
@app.post("/spellcheck")
async def spell_check(request: Request):
    data = await request.json()
    message = data.get("message", "")
    suggestions = sym_spell.lookup_compound(message, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else message

    # return ONLY the field you use in chatbot: "corrected_message"
    return {
        "corrected_message": corrected
    }
