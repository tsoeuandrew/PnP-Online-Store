import flet as ft
import requests,json

def main(page: ft.Page):
    page.title = "My Flet App"
    page.bgcolor = "black"                  
    page.window_maximized = True            
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT  # Set theme mode
    image = ft.Image(src=r"C:\\Users\\andre\\Documents\\GitHub\\PNP-ONLINE-STORE\\cover", width=150, height=150)


    def toggle_theme(e):            
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        page.update()

    def home_page(page: ft.Page):
        return ft.View(
            "/",
            controls=[
                ft.Text("Welcome to the Home Page", size=20),
                ft.Switch(label="Dark Mode", on_change=toggle_theme),
                ft.ElevatedButton("Go to Second Page", on_click=lambda e: page.go("/second"))
            ],
        )

    def second_page(page: ft.Page):
        return ft.View(
            "/second",
            controls=[
            ft.Text("This is the Second Page", size=20),
            ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/"))
            ],
        )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(home_page(page))
        elif page.route == "/second":
            page.views.append(second_page(page))
        page.update()
    
    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
