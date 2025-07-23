from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI()
MAX_QUESTIONS = 10
sessions = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id", "default")
    user_input = data.get("message", "")

    remaining = sessions.get(session_id, MAX_QUESTIONS)

    if remaining <= 0:
        return jsonify({"response": "Din spørgekvote er opbrugt. Kontakt administratoren.", "remaining": 0})

    system_prompt = f"Remaining questions: {remaining}\nHusk: hvis Remaining questions = 0, sig 'Din spørgekvote er opbrugt. Kontakt administratoren.'"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response.choices[0].message.content
    sessions[session_id] = remaining - 1

    return jsonify({"response": reply, "remaining": sessions[session_id]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
