from flask import Flask, request, jsonify
import uuid
import math
import json

app = Flask(__name__)

# In-memory storage for receipts and points
receipts_data = {}

# Process Receipts endpoint
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    try:
        # Accept both JSON and form data
        receipt_data = request.get_json() or request.form.to_dict()

        print("Received Data:", receipt_data)

        # Validate the receipt format
        validate_receipt(receipt_data)

        # Generate a unique ID for the receipt
        receipt_id = str(uuid.uuid4())

        # Store the receipt in memory
        receipts_data[receipt_id] = receipt_data

        # Return the generated ID
        response_data = {"id": receipt_id}
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get Points endpoint
@app.route('/debug/receipts', methods=['GET'])
def debug_receipts():
    return jsonify(receipts_data)
    
@app.route('/receipts/<string:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    try:
        # Lookup receipt by ID
        receipt = receipts_data.get(receipt_id)

        if receipt is None:
            return jsonify({"error": "No receipt found for that id"}), 404

        # Calculate points based on new receipt rules
        points = calculate_points(receipt)

        # Return the points awarded
        response_data = {"points": points}
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def validate_receipt(receipt_data):
    # You can implement more detailed validation logic here based on the schema
    # specified in the api.yml file. For simplicity, we're just checking the required fields.
    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    for field in required_fields:
        if field not in receipt_data:
            raise ValueError(f"Missing required field: {field}")

def calculate_points(receipt):
    points = 0

    # Rule1: One point for every alphanumeric character in the retailer name.
    points += sum(c.isalnum() for c in receipt["retailer"])

    # Rule2: 50 points if the total is a round dollar amount with no cents.
    total_float = float(receipt["total"])
    if total_float.is_integer():
        points += 50

    # Rule3: 25 points if the total is a multiple of 0.25.
    if total_float % 0.25 == 0:
        points += 25

    # Rule4: 5 points for every two items on the receipt.
    points += 5 * (len(receipt["items"]) // 2)

    # Rule5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by -0.2 and round up to the nearest integer.
    for item in receipt["items"]:
        trimmed_length = len(item["shortDescription"].strip())
        if trimmed_length % 3 == 0:
            price_points = math.ceil(float(item["price"]) * (-0.2))
            points += max(price_points, 0)

    # Rule6: 6 points if the day in the purchase date is odd.
    purchase_day = int(receipt["purchaseDate"].split("-")[2])
    if purchase_day % 2 == 1:
        points += 6

    # Rule7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    purchase_time = int(receipt["purchaseTime"].split(":")[0])
    if 14 <= purchase_time < 16:
        points += 10

    return points

if __name__ == '__main__':
    app.run(debug=True)
