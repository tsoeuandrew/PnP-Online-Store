import flet as ft
import requests
import json

def main(page: ft.Page):
    page.title = "Pick an Pay Online Store"
    page.bgcolor = "black"
    page.window_maximized = True
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.DARK

    cart = {}

    # Feedback for different fields
    username_feedback = ft.Text(color="red", weight="bold")
    id_feedback = ft.Text(color="red", weight="bold")
    feedback = ft.Text(color="green", weight="bold")
    password_feedback = ft.Text(color="red", weight="bold")
    mobile_feedback = ft.Text(color="red", weight="bold")
    gender_feedback = ft.Text(color="red", weight="bold")

    # Create input and output controls
    id_number = ft.TextField(label="Enter ID Number", autofocus=True)
    username = ft.TextField(label="Enter username")
    mobile = ft.TextField(label="Enter Mobile Number")
    password = ft.TextField(label="Enter Password")
    address = ft.TextField(label="Physical Address", height=100, multiline=True)
    # Gender dropdown
    gender = ft.Dropdown(
        label="Gender",
        value="Please Select",  # Default value (not in options list)
        options=[
            ft.dropdown.Option("Male"),
            ft.dropdown.Option("Female")
        ],
    )

    # Clear errors when submitting the form
    def clear_feedback():
        username_feedback.value = ""
        id_feedback.value = ""
        feedback.value = ""
        password_feedback.value = ""
        mobile_feedback.value = ""
        gender_feedback.value = ""

    def error_handler():
        clear_feedback()
        has_errors = False
        try:
            # Validate username
            if not username.value.strip():  # Check if the names field is empty
                username_feedback.value = "username cannot be empty."
                has_errors = True
            elif not username.value.replace(" ", "").isalpha():
                username_feedback.value = "username must only contain alphabetic characters."
                has_errors = True

            # Vlidate password
            if len(password.value) <= 4:
                password_feedback.value = "Pssword must be 4 units or grater long."
                has_errors = True

            # Validate ID Number
            id_number_cleaned = id_number.value.strip()
            if not id_number_cleaned.isdigit() or len(id_number_cleaned) != 13:
                id_feedback.value = "password must be 13 digits long and numeric."
                has_errors = True

            # Validate mobile Number
            mobile_cleaned = mobile.value.strip()
            if not mobile_cleaned.isdigit() or len(mobile_cleaned) != 10:
                mobile_feedback.value = "mobile must be 10 digits long and numeric."
                has_errors = True

            # Validate Gender selection
            if gender.value == "Please Select":
                gender_feedback.value = "Please select a Gender."
                has_errors = True

        except Exception as e:
            feedback.value = f"Unexpected Error: {str(e)}"
            has_errors = True  # Mark an error occurred

        finally:
            page.update()
        return has_errors  # Return True if errors exist, False otherwise # Check if the user has entered a valid name

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
            ft.Container(
                content=ft.Image(
                    src=product.get("image", default_image_path),
                    width=150,
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text("No image")
                ),
                on_click=lambda e, p=product: add_to_cart(p)
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

    def save_user(e):
        if error_handler():  # Check for errors
            return  # Don't save if there are errors

        info = {
            "Username": username.value,
            "Password": password.value,
            "ID Number": id_number.value,
            "Mobile Number": mobile.value,
            "Physical Address": address.value,
            "Gender": gender.value
        }

        try:
            response = requests.post("http://localhost:5000/api/save_user", json=info)
            if response.status_code == 200:
                page.go("/")  # Navigate to next page
            else:
                feedback.value = response.json().get("error", "Unknown error")
                page.update()

        except requests.exceptions.RequestException as ex:
            feedback.value = f"Error connecting to server: {str(ex)}"
            page.update()


    def Login(e):
        clear_feedback()
        has_errors = False

        # Validate username
        if not username.value.strip():
            username_feedback.value = "Username cannot be empty."
            has_errors = True
        elif not username.value.replace(" ", "").isalpha():
            username_feedback.value = "Username must only contain alphabetic characters."
            has_errors = True

        # Validate password
        if len(password.value.strip()) <= 4:
            password_feedback.value = "Password must be at least 5 characters long."
            has_errors = True

        if has_errors:
            page.update()
            return  # Exit early if there are validation issues

        try:
            # Send POST request with JSON payload
            info = {
                "Username": username.value.strip(),
                "Password": password.value.strip()
            }
            response = requests.post("http://localhost:5000/api/login", json=info)
            response_data = response.json()

            if response.status_code == 200:
                feedback.value = response_data.get("message", "Login successful.")
                page.update()
                page.go("/two")
            else:
                feedback.value = response_data.get("error", "Unknown error occurred.")
        except requests.RequestException as e:
            feedback.value = f"Error connecting to server: {str(e)}"

        page.update()


    def login_page():
        return ft.View(
            "/",
            controls=[
                ft.Text("Pick an Pay Online Store", size=50),
                username, username_feedback,
                password, password_feedback,
                feedback,
                ft.Row([
                    ft.ElevatedButton("Login", on_click=Login),
                    ft.ElevatedButton("Create new Account", on_click=lambda e: page.go("/thirteen")),
                    ft.Switch(label="Theme", on_change=toggle_theme)
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ],
        )
    
    def Register():
        return ft.View(
            "/thirteen",  # Corrected route to match "/thirteen"
            controls=[
                ft.Text("Pick an Pay Online Store", size=50),
                username, username_feedback,
                password, password_feedback,
                id_number, id_feedback,
                gender, gender_feedback,
                mobile, mobile_feedback,
                address,
                ft.Row([
                    ft.ElevatedButton("save user", on_click=save_user),
                    ft.Switch(label="Theme", on_change=toggle_theme)
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ]
        )


    def home_page():
        return ft.View(
            "/two",
            controls=[
                ft.Text("Welcome To Pick An Pay Online Store", size=50),
                ft.Switch(label="Theme", on_change=toggle_theme),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Grains and Pasta", on_click=lambda e: page.go("/ten")),
                    ft.ElevatedButton("Cosmetics", on_click=lambda e: page.go("/eleven")),
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
                    ft.ElevatedButton("Cosmetics", on_click=lambda e: page.go("/eleven")),
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
                    ft.ElevatedButton("Cosmetics", on_click=lambda e: page.go("/eleven")),
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
                    ft.ElevatedButton("Cosmetics", on_click=lambda e: page.go("/eleven")),
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
                    ft.ElevatedButton("Cosmetics", on_click=lambda e: page.go("/eleven")),
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
                    ft.ElevatedButton("Cosmetics", on_click=lambda e: page.go("/eleven")),
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
                    ft.ElevatedButton("Cosmetics", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Grains_Pasta():
        products = fetch_products("grains")
        product_columns = create_product_display(products, "grains_pasta/default.png")
        
        return ft.View(
            "/ten",
            controls=[
                ft.Text("Pick An Pay Online Store", size=70),
                ft.Text("Grains and Pasta", size=50),
                ft.Column(product_columns),
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
                    ft.ElevatedButton("Vegetables", on_click=lambda e: page.go("/four")),
                    ft.ElevatedButton("Meat", on_click=lambda e: page.go("/five")),
                    ft.ElevatedButton("Drinks", on_click=lambda e: page.go("/six")),
                    ft.ElevatedButton("Snacks", on_click=lambda e: page.go("/seven")),
                    ft.ElevatedButton("Bakery", on_click=lambda e: page.go("/eight")),
                    ft.ElevatedButton("Dairy", on_click=lambda e: page.go("/nine")),
                    ft.ElevatedButton("Cosmetics", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Breakfast", on_click=lambda e: page.go("/twelve")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Cosmetics():
        products = fetch_products("Cosmetics")
        product_columns = create_product_display(products, "cosmetics/default.png")
        
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
                    ft.ElevatedButton("Cosmetics", on_click=lambda e: page.go("/eleven")),
                    ft.ElevatedButton("Go to Cart", on_click=lambda e: page.go("/fourteen")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Cart_page():
        all_products = {}
        categories = ["fruits", "vegetables", "meat", "drinks", "snacks", "bakery", "dairy", "grains", "cosmetics", "breakfast"]
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
            page.views.append(Cosmetics())
        elif page.route == "/twelve":
            page.views.append(Breakfast())
        elif page.route == "/thirteen":
            page.views.append(Register())  
        elif page.route == "/fourteen":
            page.views.append(Cart_page())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, port=8000)