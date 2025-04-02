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

    # Open inventory file
    try:
        products_data = {}
        with open("inventory.json", "r") as file:
            products_data = json.load(file)
        print("Products loaded successfully!")
    except FileNotFoundError:
        print("Error: The file 'inventory.json' was not found.")
        with open("inventory.json", "w") as file:
            json.dump({}, file)
    except json.JSONDecodeError:
        print("Error: The file 'inventory.json' contains invalid JSON.")
        products_data = {}

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

        info = {
            "username": username.value,
            "ID Number": id_number.value,
            "Mobile Number": mobile.value,
            "Physical Address": address.value,
        }
        
        try:
            new_id = id_number.value
            try:
                with open(user_data, 'r') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []
            
            for record in data:
                if record.get("ID Number") == new_id:
                    feedback.value = "You are already in the database."
                    page.update() 
                    return
            
            data.append(info)
            with open(user_data, 'w') as file:
                json.dump(data, file, indent=4)
            feedback.value = "Data saved successfully!"
            page.go("/two")

        except Exception as e:
            feedback.value = f"Error saving data: {str(e)}"

        finally:
            page.update()

    def add_to_cart(e, product):
        product_name = product["name"]
        cart[product_name] = cart.get(product_name, 0) + 1
        page.add(ft.Text(f"Added {product_name} to cart!"))
        page.update()

    def bakery():
        price_controls = [ft.Text(f"Price: R{product['price']:.2f}") for product in products_data.get("Bakery", [])]
        name_controls = [ft.Text(product["name"], weight="bold") for product in products_data.get("Bakery", [])]
        image_controls = [
            ft.Container(
                content=ft.Image(
                    src=product.get("image", "bakery/default.png"),  # Default image if not found
                    width=150, height=150,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text("No image"),
                ),
                on_click=lambda e, prod=product: add_to_cart(e, prod)  # Use on_click to handle clicks
            ) for product in products_data.get("Bakery", [])
        ]

        product_columns = []
        for i in range(0, len(image_controls), 8):
            row = ft.Row(
                controls=[
                    ft.Column(
                        controls=[image_controls[i], name_controls[i], price_controls[i]],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                    for i in range(i, min(i + 8, len(image_controls)))
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
            product_columns.append(row)

        return ft.View(
            "/eight",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(controls=product_columns),
                ft.Row([
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Cart_page():
        # Get product details from inventory.json to match cart items
        bakery_products = {p["name"]: p for p in products_data.get("Bakery", [])}
        
        # Prepare controls for cart items
        if not cart:
            return ft.View(
                "/fourteen",
                controls=[
                    ft.Text("Pick an Pay Online Store", size=50),
                    ft.Text("Cart is empty"),
                    ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
                ],
            )

        image_controls = []
        name_controls = []
        total_price_controls = []

        for item_name, quantity in cart.items():
            product = bakery_products.get(item_name)
            if product:
                total_price = product["price"] * quantity
                image_controls.append(
                    ft.Container(
                        content=ft.Image(
                            src=product.get("image", "bakery/default.png"),
                            width=150, height=150,
                            fit=ft.ImageFit.CONTAIN,
                            error_content=ft.Text("No image"),
                        )
                    )
                )
                name_controls.append(ft.Text(f"{item_name} (x{quantity})", weight="bold"))
                total_price_controls.append(ft.Text(f"Total: R{total_price:.2f}"))

        cart_columns = []
        for i in range(0, len(image_controls), 8):
            row = ft.Row(
                controls=[
                    ft.Column(
                        controls=[image_controls[i], name_controls[i], total_price_controls[i]],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                    for i in range(i, min(i + 8, len(image_controls)))
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
            cart_columns.append(row)

        return ft.View(
            "/fourteen",
            controls=[
                ft.Text("Pick an Pay Online Store", size=50),
                ft.Column(controls=cart_columns),
                ft.Row([
                    ft.ElevatedButton("Back to Bakery", on_click=lambda e: page.go("/eight")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def save_user():
        return ft.View(
            "/thirteen",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                username, username_feedback,
                password,
                id_number, id_feedback,
                mobile,
                ft.ElevatedButton("Save", on_click=save_data),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
                feedback
            ],
        )

    def login_page():
        return ft.View(
            "/",
            controls=[
                ft.Text("Pick an Pay Online Store", size=50),
                username,
                password,
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
                ft.ElevatedButton("Create new Account", on_click=lambda e: page.go("/thirteen")),
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
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
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