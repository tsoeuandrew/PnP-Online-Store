from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# In-memory cart (for simplicity; in production, use a database)
cart = {}

#open inventory file
try:
    products_data = {}
    with open("inventory.json", "r") as file:
        products_data = json.load(file)
    print("Products loaded successfully!")
except FileNotFoundError:
    print("Error: The file 'inventory.json' was not found.")
    file = open("inventory.json", "w")              #create new inventory if no iventory found
except json.JSONDecodeError:
    print("Error: The file 'inventory.json' contains invalid JSON.")

#open user file
try:
    user_data = []
    with open("user.json", "r") as file:
        user_data = json.load(file)
    print("user loaded successfully!")
except FileNotFoundError:
    print("Error: The file 'user.json' was not found.")
    file = open("user.json", "w")              #create new user if no user found
except json.JSONDecodeError:
    print("Error: The file 'user.json' contains invalid JSON.")

@app.route('/api/save_user', methods=['POST'])
def save_user():
    user = request.get_json()
    
    # Extract and validate required fields
    username = user.get("Username", "").strip()
    password = user.get("Password","")
    id_number = user.get("ID Number", "").strip()
    mobile = user.get("Mobile Number", "").strip()
    address = user.get("Physical Address", "").strip()
    gender = user.get("Gender")

    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "password is required"}), 400
    if not id_number:
        return jsonify({"error": "ID Number is required"}), 400
    if not mobile:
        return jsonify({"error": "Mobile Number is required"}), 400
    if not address:
        return jsonify({"error": "Physical Address is required"}), 400
    if not gender:
        return jsonify({"error": "gender is required"}), 400
    
    # Check for duplicate ID
    for record in user_data:
        if record.get("ID Number") == id_number:
            return jsonify({"error": "This user already in the database"}), 400
            
    new_user = {
        "username": username,
        "Password": password,
        "ID Number": id_number,
        "Mobile Number": mobile,
        "Physical Address": address,
        "Gender": gender
    }
    user_data.append(new_user)

    # Save updated user data to file
    try:
        with open("user.json", 'w') as file:  # Fixed: correct filename
            json.dump(user_data, file, indent=4)
        return jsonify({"message": "Data saved successfully"})
    except Exception as ex:
        return jsonify({"error": f"Error saving data: {str(ex)}"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    user = request.get_json()
    
    username = user.get("Username", "")
    password = user.get("Password", "")

    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "password is required"}), 400
    
    for record in user_data:
        if record.get("Username") == username and record.get("Password") == password:
            return jsonify({
                "message": "Login successful",
                "user": {
                    "username": record["username"],
                    "id_number": record["ID Number"],
                    "mobile": record["Mobile Number"],
                    "address": record["Physical Address"],
                    "gender": record["Gender"]
                }
            }), 200
    
    # If no match is found
    return jsonify({"error": "Invalid username or password"}), 401

# Generic endpoint to get products by category
@app.route('/api/products/<category>', methods=['GET'])
def get_products(category):
    # Capitalize first letter to match your inventory structure
    formatted_category = category.capitalize()       #capitalise first letter
    category_data = products_data.get(formatted_category, [])
    return jsonify(category_data)

# Add item to cart with quantity check
@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_name = data.get('product_name')
    
    # Check if product exists in inventory and has sufficient quantity
    for category in products_data:
        for product in products_data[category]:
            if product['name'] == product_name:
                if product['quantity'] > 0:
                    if product_name in cart:
                        if product['quantity'] > cart[product_name]:
                            cart[product_name] += 1
                            return jsonify({"message": f"Added {product_name} to cart", "cart": cart})
                        else:
                            return jsonify({"error": f"Insufficient quantity of {product_name}"}), 400
                    else:
                        cart[product_name] = 1
                        return jsonify({"message": f"Added {product_name} to cart", "cart": cart})
                else:
                    return jsonify({"error": f"{product_name} is out of stock"}), 400
    return jsonify({"error": f"Product {product_name} not found"}), 404

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

if __name__ == '__main__': 
    app.run(debug=True, port=5000)