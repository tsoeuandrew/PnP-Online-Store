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

    # Function to fetch products from Flask
    def fetch_products(category):
        try:
            response = requests.get(f"http://localhost:5000/api/products/{category.lower()}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch {category}: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Error fetching {category}: {e}")
            return []

    # Reusable function to create product display
    def create_product_display(products, default_image_path):
        price_controls = [ft.Text(f"Price: R{product['price']:.2f}") for product in products]
        name_controls = [ft.Text(product["name"], weight="bold") for product in products]
        image_controls = [
            ft.Image(
                src=product.get("image", default_image_path),
                width=150, height=150,
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.Text("No image")
            ) for product in products
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
        
        return product_columns

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
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ],
        )

    def fruits():
        products = fetch_products("fruits")
        product_columns = create_product_display(products, "fruits/default.png")
        
        return ft.View(
            "/third",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Vegetables():
        products = fetch_products("vegetables")
        product_columns = create_product_display(products, "vegetables/default.png")
        
        return ft.View(
            "/four",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def meat():
        products = fetch_products("meat")
        product_columns = create_product_display(products, "meat/default.png")
        
        return ft.View(
            "/five",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def drinks():
        products = fetch_products("drinks")
        product_columns = create_product_display(products, "drinks/default.png")
        
        return ft.View(
            "/six",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def snacks():
        products = fetch_products("snacks")
        product_columns = create_product_display(products, "snacks/default.png")
        
        return ft.View(
            "/seven",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def bakery():
        products = fetch_products("bakery")
        product_columns = create_product_display(products, "bakery/default.png")
        
        return ft.View(
            "/eight",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def dairy():
        products = fetch_products("dairy")
        product_columns = create_product_display(products, "dairy/default.png")
        
        return ft.View(
            "/nine",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Grains_Pasta():
        products = fetch_products("grains & pasta")
        product_columns = create_product_display(products, "grains_pasta/default.png")
        
        return ft.View(
            "/ten",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Bath_Stuff():
        products = fetch_products("bath stuff")
        product_columns = create_product_display(products, "bath_stuff/default.png")
        
        return ft.View(
            "/eleven",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Breakfast():
        products = fetch_products("breakfast")
        product_columns = create_product_display(products, "breakfast/default.png")
        
        return ft.View(
            "/twelve",
            controls=[
                ft.Text("Pick An Pay Online Store", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Bath Stuff", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Cart_page():
        all_products = {}
        categories = ["fruits", "vegetables", "meat", "drinks", "snacks", "bakery", "dairy", "grains & pasta", "bath stuff", "breakfast"]
        for category in categories:
            products = fetch_products(category)
            all_products.update({p["name"]: p for p in products})

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
            product = all_products.get(item_name)
            if product:
                total_price = product["price"] * quantity
                image_controls.append(
                    ft.Container(
                        content=ft.Image(
                            src=product.get("image", "default.png"),
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

    def add_to_cart(page, product):
        product_name = product["name"]
        cart[product_name] = cart.get(product_name, 0) + 1
        page.add(ft.Text(f"Added {product_name} to cart!"))
        page.update()

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
        elif page.route == "/third":
            page.views.append(fruits())
        elif page.route == "/four":
            page.views.append(Vegetables())
        elif page.route == "/five":
            page.views.append(meat())
        elif page.route == "/six":
            page.views.append(drinks())
        elif page.route == "/seven":
            page.views.append(snacks())
        elif page.route == "/eight":
            page.views.append(bakery())
        elif page.route == "/nine":
            page.views.append(dairy())
        elif page.route == "/ten":
            page.views.append(Grains_Pasta())
        elif page.route == "/eleven":
            page.views.append(Bath_Stuff())
        elif page.route == "/twelve":
            page.views.append(Breakfast())
        elif page.route == "/thirteen":
            page.views.append(save_user())
        elif page.route == "/fourteen":
            page.views.append(Cart_page())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, port=8000)