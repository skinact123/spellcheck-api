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

# Webhook (GET for verification, POST for processing)
@app.api_route("/spellcheck", methods=["GET", "POST"])
async def spellcheck(request: Request, challenge: str = "", token: str = ""):
    if request.method == "GET":
        return Response(content=challenge, media_type="text/plain")

    data = await request.json()
    print("Received:", data)
    input_text = data.get("message", "")
    suggestions = sym_spell.lookup_compound(input_text, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else input_text

    # ✅ Return what ChatBot expects
    return {"message": corrected}
