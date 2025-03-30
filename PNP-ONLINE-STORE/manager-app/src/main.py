import flet as ft
import requests
import json

def main(page: ft.Page):
    page.title = "PnP Manager Portal"
    page.bgcolor = "black"
    page.window_maximized = True
    page.theme_mode = ft.ThemeMode.DARK

    # Single set of input fields for managing products
    product_input = ft.TextField(label="Product Name")  # Product name to add or update
    quantity_input = ft.TextField(label="Quantity", value="0")  # Stock level
    price_input = ft.TextField(label="Price", value="0.0")      # Price (used only for new products)
    output = ft.Text()  # Display success or error messages

   # Function to manage the product (add or update, including price)
    def manage_product(e):
        product = product_input.value.lower()  # Get product name (lowercase for consistency)
        try:
            quantity = int(quantity_input.value)  # Convert quantity to integer
            price = float(price_input.value)      # Convert price to float
            # Send POST request to the combined endpoint
            response = requests.post(
                "http://localhost:5000/api/manage_product",
                json={"product": product, "quantity": quantity, "price": price}
            )
            # Show the response message (success or error)
            output.value = response.json().get("message") or response.json().get("error")
        except ValueError:
            output.value = "Invalid quantity or price"  # Handle invalid inputs
        page.update()  # Refresh the page to show the output

    # Add controls to the page
    page.add(
        ft.Image(src="cover.jpg", width=150, height=150),  # Display an image
        ft.Text("Pick n Pay Manager Portal", size=30),     # Title
        ft.Row([product_input, quantity_input, price_input]),  # One row of inputs
        ft.ElevatedButton("Manage Product", on_click=manage_product),  # One button
        output                                             # Output message
    )

ft.app(target=main, port=5000)