import flet as ft
from pages.home import home_page


def main(page: ft.Page):
    home_page(page)


ft.app(target=main, upload_dir="uploads", assets_dir="assets")