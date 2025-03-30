from flask import Flask, jsonify, request

app = Flask(__name__)

products = me.json

# Endpoint for customers to view products
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

# Endpoint for customers to place an order
@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    product_name = data.get("product")
    quantity = data.get("quantity", 1)
    
    if product_name not in products:
        return jsonify({"error": "Product not found"}), 404
    if products[product_name]["quantity"] < quantity:
        return jsonify({"error": "Not enough stock"}), 400
    
    products[product_name]["quantity"] -= quantity
    total_cost = products[product_name]["price"] * quantity
    return jsonify({
        "message": f"Ordered {quantity} {product_name}(s) successfully",
        "total_cost": total_cost
    })


# Endpoint for managers to add or update products (now with category)
@app.route('/api/manage_product', methods=['POST'])
def manage_product():
    data = request.json
    product_name = data.get("product")      # Product name
    quantity = data.get("quantity", 0)      # Quantity
    price = data.get("price", 0.0)          # Price
    category = data.get("category", "Other") # Category (default to "Other" if not provided)

    # If product exists, update quantity, price, and category
    if product_name in products:
        products[product_name]["quantity"] = quantity
        products[product_name]["price"] = price
        products[product_name]["category"] = category
        return jsonify({"message": f"Updated {product_name} to {quantity} in stock, price ${price}, category {category}"})
    # If product doesn’t exist, add it
    else:
        products[product_name] = {"quantity": quantity, "price": price, "category": category}
        return jsonify({"message": f"Added {product_name} with {quantity} in stock, price ${price}, category {category}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)