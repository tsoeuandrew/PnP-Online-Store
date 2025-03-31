import flet as ft
import requests
import json

def main(page: ft.Page):
    page.title = "Pick an Pay Online Store"
    page.bgcolor = "black"                   
    page.window_maximized = True            
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.DARK

    image = ft.Image(src="cover.jpg", width=150, height=150)

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

    #open products file
    try:
        with open("products.json", "r") as file:
            products_data = json.load(file)
        print("Products loaded successfully!")
    except FileNotFoundError:
        print("Error: The file 'products.json' was not found.")
    except json.JSONDecodeError:
        print("Error: The file 'products.json' contains invalid JSON.")

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
                image,
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
                image,
                ft.Text("Pick an Pay Online Store", size=30),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                )
            ],
        )
    
    def fruits():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Fruits", [])]
        return ft.View(
            "/third",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),           #end row
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def Vegetables():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Vegetables", [])]
        return ft.View(
            "/four",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def meat():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Meat", [])]
        return ft.View(
            "/five",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def drinks():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Drinks", [])]
        return ft.View(
            "/six",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def snacks():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Snacks", [])]
        return ft.View(
            "/seven",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def bakery():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Bakery", [])]
        return ft.View(
            "/eight",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def dairy():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Dairy", [])]
        return ft.View(
            "/nine",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )

    def Grains_Pasta():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Grains & Pasta", [])]
        return ft.View(
            "/ten",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def Bath_Stuff():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Bath Stuff", [])]
        return ft.View(
            "/eleven",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def Breakfast():
        product_controls = [ft.Text(product["name"]) for product in products_data.get("Breakfast", [])]
        return ft.View(
            "/twelve",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                ft.Column(product_controls),
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
                ],scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.CENTER,spacing=10
                ),
                ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/two")),
            ],
        )
    
    def save_user():
        return ft.View(
            "/thirteen",
            controls=[
                image,
                ft.Text("Pick an Pay Online Store", size=30),
                username,
                password,
                id_number,
                mobile,
                ft.ElevatedButton("Login", on_click=save_data),
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
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, port=5000)