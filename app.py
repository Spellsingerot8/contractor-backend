from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Contractor-in-a-Can backend is running!"})

@app.route('/flooring-estimate', methods=['POST'])
def flooring_estimate():
    data = request.json
    sqft = data.get('square_feet', 0)
    zip_code = data.get('zip', '00000')

    # Sample price range (adjust later based on zip)
    material_price = 4.0  # per square foot
    labor_price = 2.5     # per square foot

    material_cost = sqft * material_price
    labor_cost = sqft * labor_price
    total_cost = material_cost + labor_cost

    return jsonify({
        "square_feet": sqft,
        "material_cost": round(material_cost, 2),
        "labor_cost": round(labor_cost, 2),
        "total_cost": round(total_cost, 2)
    })

if __name__ == '__main__':
    app.run()
