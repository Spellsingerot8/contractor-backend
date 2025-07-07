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

def ask_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful contractor estimation assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route("/flooring", methods=["POST"])
def flooring_estimate():
    data = request.get_json()
    width = data.get("width")
    length = data.get("length")
    quality = data.get("quality")

    if not all([width, length, quality]):
        return jsonify({"error": "Missing input values."}), 400

    prompt = f"I need a flooring estimate for a {width}x{length} ft room using {quality} flooring."
    result = ask_openai(prompt)
    return jsonify({"result": result})

@app.route("/drywall", methods=["POST"])
def drywall_estimate():
    data = request.get_json()
    width = data.get("width")
    height = data.get("height")
    quality = data.get("quality")

    if not all([width, height, quality]):
        return jsonify({"error": "Missing input values."}), 400

    prompt = f"Estimate cost and materials for drywalling a {width}x{height} ft wall using {quality} materials."
    result = ask_openai(prompt)
    return jsonify({"result": result})

@app.route("/painting", methods=["POST"])
def painting_estimate():
    data = request.get_json()
    width = data.get("width")
    height = data.get("height")
    surface = data.get("surface", "exterior wall")
    quality = data.get("quality", "standard")

    if not all([width, height]):
        return jsonify({"error": "Missing dimensions."}), 400

    prompt = f"Estimate how much paint is needed and cost to paint a {width}x{height} ft {surface} using {quality} paint."
    result = ask_openai(prompt)
    return jsonify({"result": result})

@app.route("/tile", methods=["POST"])
def tile_layout():
    data = request.get_json()
    room_width = data.get("room_width")
    room_length = data.get("room_length")
    tile_width = data.get("tile_width")
    tile_length = data.get("tile_length")

    if not all([room_width, room_length, tile_width, tile_length]):
        return jsonify({"error": "Missing input values."}), 400

    prompt = f"Calculate how many {tile_width}x{tile_length} inch tiles are needed to cover a {room_width}x{room_length} foot floor. Include 10% overage."
    result = ask_openai(prompt)
    return jsonify({"result": result})

@app.route("/convert", methods=["POST"])
def measurement_converter():
    data = request.get_json()
    input_text = data.get("text")

    if not input_text:
        return jsonify({"error": "Missing text input."}), 400

    prompt = f"Convert the following measurement: {input_text}"
    result = ask_openai(prompt)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run()
