import flet as ft
import requests
import json

def main(page: ft.Page):
    page.title = "Pick an Pay Online Store"
    page.bgcolor = "black"                   
    page.window_maximized = True            
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.DARK

    # Feedback for different fields
    username_feedback = ft.Text(color="red", weight="bold")
    id_feedback = ft.Text(color="red", weight="bold")
    feedback = ft.Text(color="red", weight="bold")

    # Clear errors when submitting the form
    def clear_feedback():
        username_feedback.value = ""
        id_feedback.value = ""
        feedback.value = ""
    
    # Create input and output controls
    id_number = ft.TextField(label="Enter ID Number", autofocus=True)
    input_box = ft.TextField(label="Enter name")
    username = ft.TextField(label="Enter username")
    mobile = ft.TextField(label="Enter Mobile Number")
    password = ft.TextField(label="Enter Password")
    address = ft.TextField(label="Physical Address", height=100, multiline=True)
    output = ft.Text()

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

    def toggle_theme(e):                    
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()

    def send_name(e):
        response = requests.post("http://localhost:5000/api/hello", json={"name": input_box.value})
        output.value = response.json().get("reply")
        page.update()

    def save_data(e):
        clear_feedback()
        user_data = "data.json"

        # Prepare the user data to be saved as a dictionary
        info = {
            "username": username.value,
            "ID Number": id_number.value,
            "Mobile Number": mobile.value,
            "Physical Address": address.value,
        }
        
        try:
            new_id = id_number.value  # Get the ID from the input field to search for duplicates
            try:
                with open(user_data, 'r') as file:  # Open the file in read mode
                    data = json.load(file)  # Load existing JSON data
            except (FileNotFoundError, json.JSONDecodeError):
                data = []    #If file doesn't exist or is invalid, initialize an empty list
            
            for record in data:  # Loop through each record in the data
                if record.get("ID Number") == new_id:  # ID found
                    feedback.value = "You are already in the database."
                    page.update() 
                    return  # Exit the loop after finding the ID
            
            data.append(info)  # Append the new user info to the list
            with open(user_data, 'w') as file:  # Open the file and rewrite the updated data
                json.dump(data, file, indent=4)  # Save the list with indentation for readability
            feedback.value = "Data saved successfully!"  # Success feedback
            page.go("/two")  # Go to home page

        except Exception as e:
            feedback.value = f"Error saving data: {str(e)}"  # Error feedback

        finally:
            page.update()  # Update the page to reflect the feedback

    def login_page():
        return ft.View(
            "/",
            controls=[
                ft.Text("Pick an Pay Online Store", size=50),
                username,
                password,
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
                ft.ElevatedButton("Create new Acount", on_click=lambda e: page.go("/thirteen")),
                ft.Switch(label="Theme", on_change=toggle_theme)
            ],
        )

    def home_page():
        return ft.View(
            "/two",
            controls=[
                ft.Text("Welcome To Pick An Pay Online Store", size=50),
                ft.Switch(label="Theme", on_change=toggle_theme),
                input_box,
                ft.ElevatedButton("Send", on_click=send_name),
                output,
                ft.Row([
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                )
            ],
        )
    
    def bakery():
        price_controls = [ft.Text(f"Price: R{product['price']:.2f}") for product in products_data.get("Bakery", [])]
        name_controls = [ft.Text(product["name"], weight="bold") for product in products_data.get("Bakery", [])]
        image_controls = [
            ft.Image(   # Get image source from the product, or use a default if not available
                src=product.get("image", product.get("ïmage", "bakery/default.png")),  # Default path if no image
                width=150, height=150,  # Image dimensions
                fit=ft.ImageFit.CONTAIN,  # Ensure the image fits within the defined size
                error_content=ft.Text("No image")  # Text to display if the image can't be loaded
            ) for product in products_data.get("Bakery", [])  # Loop over all products in the "Bakery" category
        ]

        # Group the products into rows, with each row containing 8 items (image, name, and price)
        product_columns = []
        for i in range(0, len(image_controls), 8):  # Loop over the image controls in chunks of 8
            row = ft.Row(
                controls=[  # Create a column for each product
                    ft.Column(
                        controls=[image_controls[i], name_controls[i], price_controls[i]],  # Each product has its image, name, and price
                        alignment=ft.MainAxisAlignment.CENTER  # Center the content within each column
                    )
                    for i in range(i, min(i + 8, len(image_controls)))  # Handle a partial row if the last chunk is less than 8 items
                ],
                alignment=ft.MainAxisAlignment.CENTER  # Center the entire row horizontally
            )
            product_columns.append(row)  # Add the row to the list of rows

        return ft.View(
            "/eight",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(
                    controls=product_columns),         #view image and price under same thing
                ft.Row([
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def Cart_page():
        return ft.View(
            "/fourteen",
            controls=[
                ft.Text("Pick an Pay Online Store", size=50),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def add_to_cart(page, product):
        product_name = product["name"]       #Retrieves the "name" key from the product dictionary
        cart[product_name] = cart.get(product_name, 0) + 1  # Checks if product_name already exists in cart.     
        page.add(ft.Text(f"Added {product_name} to cart!"))    #If it doesn’t exist, initializes it with a quantity of 1.
        page.update()                                          #If it exists, increments the quantity by 1.
    
    def save_user():
        return ft.View(
        "/thirteen",
        controls=[
            ft.Text("Pick An Pay Online Store", size=50),
            username, username_feedback,
            password,
            id_number, id_feedback,
            mobile,
            ft.ElevatedButton("save", on_click=save_data),
            ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            feedback
        ],
    )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(login_page())
        elif page.route == "/two":
            page.views.append(home_page())
        elif page.route == "/eight":
            page.views.append(bakery())
        elif page.route == "/thirteen":
            page.views.append(save_user())
        elif page.route == "/fourteen":
            page.views.append(Cart_page())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, port=5000)