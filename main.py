from fastapi import FastAPI, Request
from symspellpy.symspellpy import SymSpell, Verbosity

app = FastAPI()
sym_spell = SymSpell(max_dictionary_edit_distance=2)
sym_spell.load_dictionary("frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)

@app.get("/")
def read_root():
    return {"status": "Spellcheck API is running!"}

@app.post("/")
async def correct_spelling(req: Request):
    data = await req.json()
    user_input = data.get("message", "")
    suggestions = sym_spell.lookup(user_input, Verbosity.CLOSEST, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else user_input
    return {"messages": [{"text": corrected}]}
