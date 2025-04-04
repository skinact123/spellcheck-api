from fastapi import FastAPI, Request
from symspellpy.symspellpy import SymSpell, Verbosity
import uvicorn
import os

app = FastAPI()

# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# Load dictionary (ensure you upload frequency_dictionary_en_82_765.txt to Render)
dict_path = "frequency_dictionary_en_82_765.txt"
if os.path.exists(dict_path):
    sym_spell.load_dictionary(dict_path, term_index=0, count_index=1)
else:
    raise FileNotFoundError("Dictionary file not found")

@app.post("/spellcheck")
async def spell_check(request: Request):
    data = await request.json()
    input_text = data.get("text", "")

    suggestions = sym_spell.lookup_compound(input_text, max_edit_distance=2)
    corrected = suggestions[0].term if suggestions else input_text

    return {"corrected": corrected}

# For local development
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
