from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

def call_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message["content"]

@app.route('/')
def home():
    return "Contractor-in-a-Can Backend is Running!"

@app.route('/contractor-tool', methods=['POST'])
def contractor_tool():
    data = request.json
    tool = data.get("tool", "")
    width = data.get("width", 0)
    length = data.get("length", 0)
    height = data.get("height", 8)
    quality = data.get("quality", "mid")
    exclusions = data.get("exclusions", 0)

    area = (width * length) - exclusions

    prompt = f"""
    You are a professional {tool} estimator.
    The room is {width} ft by {length} ft, with {height} ft ceilings.
    The user chose {quality} quality materials.
    Exclude {exclusions} sq ft for doors/windows.

    Estimate the materials needed and total cost (materials + labor).
    Be specific with units (e.g., drywall sheets, gallons of paint, sq ft of flooring).
    """

    result = call_gpt(prompt)

    return jsonify({
        "tool": tool,
        "area": area,
        "response": result
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
