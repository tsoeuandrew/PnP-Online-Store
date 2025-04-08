import flet as ft
import requests
import json

def main(page: ft.Page):
    page.title = "Pick an Pay Online Store"
    page.bgcolor = "black"
    page.window_maximized = True
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.DARK

    #fitch all products from server
    all_products = {}
    categories = ["fruits", "vegetables", "meat", "drinks", "snacks", "bakery", "dairy", "grains", "cosmetics", "breakfast"]
    for category in categories:
        try:
            response = requests.get(f"http://localhost:5000/api/products/{category.lower()}")
            if response.status_code == 200:
                all_products.update({p["name"]: p for p in response.json()})
            else:
                print(f"Failed to fetch {category}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching {category}: {e}")

    #Feedback controls
    login_feedback = ft.Text(color="red", weight="bold")
    stock_feedback = ft.Text(color="green", weight="bold")
    feedback = ft.Text(color="red", weight="bold")



    # Input controls for login
    username = ft.TextField(label="Manager Username", autofocus=True)
    password = ft.TextField(label="Manager Password", password=True)
    product_name = ft.TextField(label="Product Name")
    product_price = ft.TextField(label="Price (R)")
    product_quantity = ft.TextField(label="Quantity")
    product_category = ft.Dropdown(
        label="Category",
        options=[
            ft.dropdown.Option("Fruits"),
            ft.dropdown.Option("Vegetables"),
            ft.dropdown.Option("Meat"),
            ft.dropdown.Option("Drinks"),
            ft.dropdown.Option("Snacks"),
            ft.dropdown.Option("Bakery"),
            ft.dropdown.Option("Dairy"),
            ft.dropdown.Option("Grains"),
            ft.dropdown.Option("Cosmetics"),
            ft.dropdown.Option("Breakfast"),
            ft.dropdown.Option("Household")
        ]
    )

    def clear_feedback():
        login_feedback.value = ""
        stock_feedback.value = ""
        feedback = ""

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()

    def Login(e):
        clear_feedback()
        has_errors = False

        # Validate username
        if not username.value.strip():
            login_feedback.value = "Username cannot be empty."
            has_errors = True
        elif not username.value.replace(" ", "").isalpha():
            login_feedback.value = "Username must only contain alphabetic characters."
            has_errors = True

        # Validate password
        if len(password.value.strip()) <= 4:
            login_feedback.value = "Password must be at least 5 characters long."
            has_errors = True

        if has_errors:
            page.update()
            return  # Exit early if there are validation issues

        try:
            # Send POST request with JSON 
            info = {
                "Username": username.value.strip(),
                "Password": password.value
            }
            response = requests.post("http://localhost:5000/api/manager/login", json=info)
            response_data = response.json()

            if response.status_code == 200:
                feedback.value = response_data
                page.update()
                page.go("/two")
            else:
                feedback.value = response_data
        except requests.RequestException as e:
            feedback.value = f"Error connecting to server: {str(e)}"

        page.update()

    def login_page():
        return ft.View(
            "/",
            controls=[
                ft.Text("Pick an Pay Online Store", size=50),
                username, 
                password, 
                login_feedback,
                ft.Row([
                    ft.ElevatedButton("Login", on_click=Login),
                    ft.Switch(label="Theme", on_change=toggle_theme)
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ],
        )

    def home_page():
        return ft.View(
            "/two",
            controls=[
                ft.Text("Welcome To Pick An Pay Online Store", size=50),
                ft.Switch(label="Theme", on_change=toggle_theme),
                ft.Row([
                    ft.ElevatedButton("Stock", on_click=lambda e: page.go("/third")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ],
        )

    def stock():
        return ft.View(
            "/third",
            controls=[
                ft.Text("Welcome To Pick An Pay Online Store", size=50),
                ft.Switch(label="Theme", on_change=toggle_theme),
                ft.Row([
                    ft.ElevatedButton("Back to home", on_click=lambda e: page.go("/two")),
                ], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ],
        )

    def route_change(route):  
        page.views.clear()
        if page.route == "/":
            page.views.append(login_page())  
        elif page.route == "/two":
            page.views.append(home_page())
        elif page.route == "/third":
            page.views.append(stock())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, port=8000)