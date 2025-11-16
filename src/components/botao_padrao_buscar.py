# D:\Projetos\TrenView\src\components\botao_padrao_buscar.py
import flet as ft

class BotaoPadraoBuscar(ft.ElevatedButton):
    def __init__(self, texto: str = "Buscar", icon=None, on_click=None, col=None, tooltip: str = "", **kwargs):
        # estilo fixo ou parcialmente customizável
        style = ft.ButtonStyle(
            color={
                ft.ControlState.FOCUSED: ft.Colors.BLACK,
                ft.ControlState.DEFAULT: ft.Colors.GREY_900,
            },
            bgcolor={
                ft.ControlState.HOVERED: ft.Colors.BLUE_GREY_100,
                ft.ControlState.DEFAULT: ft.Colors.AMBER,
            },
            padding={
                ft.ControlState.DEFAULT: ft.Padding(10, 10, 10, 10),
                ft.ControlState.HOVERED: ft.Padding(20, 20, 20, 20),
            },
            animation_duration=300,
            side={
                ft.ControlState.HOVERED: ft.BorderSide(width=1, color=ft.Colors.GREY_300),
                ft.ControlState.DEFAULT: ft.BorderSide(width=2, color=ft.Colors.AMBER_300),
            },
            shape={
                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=15),
                ft.ControlState.HOVERED: ft.ContinuousRectangleBorder(radius=20),
            },
        )

        super().__init__(
            text=texto,
            icon=icon,
            tooltip=tooltip,
            style=style,
            on_click=on_click,
            **kwargs
        )

        if col is not None:
            self.col = col