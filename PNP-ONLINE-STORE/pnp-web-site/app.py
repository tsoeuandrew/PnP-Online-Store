from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# In-memory cart (for simplicity; in production, use a database)
cart = {}

# Load inventory data
try:
    with open("inventory.json", "r") as file:
        products_data = json.load(file)
    print("Products loaded successfully!")
except FileNotFoundError:
    print("Error: The file 'inventory.json' was not found.")
    with open("inventory.json", "w") as file:
        json.dump({}, file)  # Create an empty inventory
    products_data = {}
except json.JSONDecodeError:
    print("Error: The file 'inventory.json' contains invalid JSON.")
    products_data = {}

# Generic endpoint to get products by category
@app.route('/api/products/<category>', methods=['GET'])
def get_products(category):
    category_data = products_data.get(category, [])
    return jsonify(category_data)

# Add item to cart
@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_name = data.get('product_name')
    if product_name in cart:
        cart[product_name] += 1
    else:
        cart[product_name] = 1
    return jsonify({"message": f"Added {product_name} to cart", "cart": cart})

# Get cart contents
@app.route('/api/cart', methods=['GET'])
def get_cart():
    return jsonify(cart)

# Example: Hello endpoint (from your original frontend)
@app.route('/api/hello', methods=['POST'])
def hello():
    data = request.get_json()
    name = data.get('name', 'Guest')
    return jsonify({"reply": f"Hello, {name}!"})

if __name__ == '__main__':  # Fixed typo: '_main_' -> '__main__'
    app.run(debug=True, port=5000)