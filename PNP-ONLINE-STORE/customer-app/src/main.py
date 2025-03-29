import flet as ft
import requests,json


def main(page: ft.Page):
    # Set page properties for mobile-like window size
    page.title = "Pick an Pay Online Store"
    page.window_full_screen = True  # Enable fullscreen mode
    page.window_resizable = True  # Allow resizing
    page.scroll = ft.ScrollMode.ALWAYS  # Enable scrolling for the entire page


   
    page.add(
        ft.SafeArea(
            ft.Container(
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)
