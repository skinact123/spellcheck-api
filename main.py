from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from symspellpy.symspellpy import SymSpell, Verbosity

app = FastAPI()

# Load SymSpell dictionary
sym_spell = SymSpell(max_dictionary_edit_distance=2)
sym_spell.load_dictionary("frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)

# Webhook verification for Chatbot.com
@app.get("/", response_class=PlainTextResponse)
def verify_webhook(challenge: str = "", token: str = ""):
    return challenge

# Spellcheck POST handler
@app.post("/")
async def correct_spelling(req: Request):
    data = await req.json()
    user_input = data.get("message", "")
    suggestions = sym_spell.lookup(user_input, Verbosity.CLOSEST, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else user_input
    # Return plain corrected text — no "messages"
    return {"text": corrected}
