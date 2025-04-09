from fastapi import FastAPI, Request
from symspellpy.symspellpy import SymSpell, Verbosity

app = FastAPI()

sym_spell = SymSpell(max_dictionary_edit_distance=2)
sym_spell.load_dictionary("frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)

@app.get("/")
def verify_webhook(challenge: str = "", token: str = ""):
    return challenge

@app.post("/")
async def correct_input(req: Request):
    data = await req.json()
    user_input = data.get("message")
    if user_input is None and len(data) > 0:
        user_input = list(data.values())[0]
    if not isinstance(user_input, str):
        user_input = ""

    suggestions = sym_spell.lookup(user_input, Verbosity.CLOSEST, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else user_input

    # ✅ Return corrected input as if it was typed by the user
    return { "corrected_input": corrected }
