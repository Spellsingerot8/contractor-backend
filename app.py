from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return "Contractor-in-a-Can backend is live."

@app.route("/contractor-tool", methods=["POST"])
def contractor_tool():
    try:
        data = request.get_json()
        tool = data.get("tool")
        width = data.get("width")
        length = data.get("length")
        quality = data.get("quality")

        if not all([tool, width, length, quality]):
            return jsonify({"error": "Missing input values."}), 400

        messages = [
            {"role": "system", "content": "You are a helpful contractor estimation assistant."},
            {"role": "user", "content": f"I need a cost estimate for {tool} for a {width} by {length} foot area using {quality} materials."}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        result = response.choices[0].message.content.strip()
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
