import flet as ft
import json

def main(page: ft.Page):
    page.title = "Pick an Pay Online Store"
    page.bgcolor = "black"                   
    page.window_maximized = True            
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.DARK

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

    def login_page():
        return ft.View(
            "/",
            controls=[
                ft.Text("Pick an Pay Online Store", size=50),
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
                ft.Row([
                    ft.ElevatedButton("Fruits", on_click=lambda e: page.go("/third")),
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
                on_click=add_to_cart,  # Assign the function here
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
                    ft.ElevatedButton("Go to cart", on_click=lambda e: page.go("/fourteen")),
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
    
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(login_page())
        elif page.route == "/two":
            page.views.append(home_page())
        elif page.route == "/eight":
            page.views.append(bakery())
        elif page.route == "/fourteen":
            page.views.append(Cart_page())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, port=5000)