from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
INVENTORY_FILE = "inventory.json"

# Load inventory from JSON file
def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return {"products": []}
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)

# Save inventory to JSON file
def save_inventory(data):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# API: Get all products
@app.route('/products', methods=['GET'])
def get_products():
    inventory = load_inventory()
    return jsonify(inventory["products"])

# API: Place an order
@app.route('/order', methods=['POST'])
def place_order():
    inventory = load_inventory()
    data = request.get_json()
    product_id = data['product_id']
    quantity = int(data['quantity'])
    
    for product in inventory["products"]:
        if product["id"] == product_id:
            if product["stock"] >= quantity:
                product["stock"] -= quantity
                save_inventory(inventory)
                return jsonify({"message": f"Ordered {quantity} of {product['name']} successfully!"})
            else:
                return jsonify({"error": "Not enough stock!"}, 400)
    return jsonify({"error": "Product not found!"}, 404)

# API: Add a new product
@app.route('/add_product', methods=['POST'])
def add_product():
    inventory = load_inventory()
    data = request.get_json()
    new_product = {
        "id": str(len(inventory["products"]) + 1),  # Simple ID generation
        "name": data['name'],
        "stock": int(data['stock']),
        "price": float(data['price'])
    }
    inventory["products"].append(new_product)
    save_inventory(inventory)
    return jsonify({"message": f"Added {new_product['name']} to inventory!"})

# API: Update stock
@app.route('/update_stock', methods=['POST'])
def update_stock():
    inventory = load_inventory()
    data = request.get_json()
    product_id = data['product_id']
    new_stock = int(data['new_stock'])
    
    for product in inventory["products"]:
        if product["id"] == product_id:
            product["stock"] = new_stock
            save_inventory(inventory)
            return jsonify({"message": f"Updated stock for {product['name']} to {new_stock}!"})
    return jsonify({"error": "Product not found!"}, 404)

if __name__ == '__main__':
    app.run(debug=True, port=5000)