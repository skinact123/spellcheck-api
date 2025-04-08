from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/spellcheck", methods=["POST"])
def spellcheck():
    try:
        data = request.get_json()

        user_message = data.get("message", "").lower()
        
        # Simple correction logic (example)
        corrections = {
            "hellooo": "hello",
            "recieve": "receive",
            "teh": "the",
            "adress": "address"
        }

        corrected_message = corrections.get(user_message, user_message)
        
        # Must return only allowed fields
        return jsonify({
            "fulfillmentText": f"Corrected: {corrected_message}"
        })

    except Exception as e:
        return jsonify({
            "fulfillmentText": f"Error: {str(e)}"
        })

@app.route("/spellcheck", methods=["GET"])
def verify():
    challenge = request.args.get("challenge")
    return challenge or "No challenge"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
