from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from symspellpy.symspellpy import SymSpell, Verbosity

app = FastAPI()

# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2)
sym_spell.load_dictionary("frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)

# Challenge verification for Chatbot.com
@app.get("/", response_class=PlainTextResponse)
def verify_webhook(challenge: str = "", token: str = ""):
    return challenge

# Pre-processing: correct user input
@app.post("/")
async def correct_input(req: Request):
    data = await req.json()
    
    # Get the message or fallback
    user_input = data.get("message")
    if user_input is None and len(data) > 0:
        user_input = list(data.values())[0]
    if not isinstance(user_input, str):
        user_input = ""

    suggestions = sym_spell.lookup(user_input, Verbosity.CLOSEST, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else user_input

    # ✅ IMPORTANT: return corrected text using "message" key
    return { "message": corrected }
