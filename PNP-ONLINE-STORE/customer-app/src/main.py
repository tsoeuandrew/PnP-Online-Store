import flet as ft
import requests,json

def main(page: ft.Page):
    page.title = "My Flet App"
    page.bgcolor = "lightblue"
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False

    btn = ft.ElevatedButton("Click Me", on_click=lambda e: print("Button clicked!"))
    page.add(btn)
    page.update()

ft.app(target=main)

ft.app(main)
