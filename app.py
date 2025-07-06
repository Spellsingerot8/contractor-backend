from flask import Flask, request, jsonify
import openai
import os
import json

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
    return jsonify({"message": "Contractor-in-a-Can backend is running!"})

@app.route('/contractor-tool', methods=['POST'])
def contractor_tool():
    data = request.json
    tool = data.get("tool", "general")
    
    # Format all inputs into readable job details
    job_details = json.dumps(data, indent=2)

    prompt = f"""
    You are a professional licensed {tool} contractor.
    Based on the following job details, provide:
    - A list of materials needed
    - Labor estimate
    - Total cost (materials + labor)
    - Optional tips or notes

    Job Details:
    {job_details}
    """

    result = call_gpt(prompt)

    return jsonify({
        "tool": tool,
        "input": data,
        "response": result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
