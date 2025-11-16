# D:\Projetos\TrenView\src\components\search_form.py
import flet as ft
from components.botao_padrao_buscar import BotaoPadraoBuscar

class SearchForm(ft.ResponsiveRow):
    def __init__(self, on_search_click, **kwargs):
        super().__init__(**kwargs)
        self.codigo_field = ft.TextField(
            col={'xs':12, 'sm':3, 'md':2, 'lg':2, 'xl':2, 'xxl':2},
            label="Controle",
            height=50,
            hint_text="Digite o código para buscar",
        )
        self.nome_field = ft.TextField(
            col={'xs':12, 'sm':6, 'md':8, 'lg':8, 'xl':8, 'xxl':8},
            label="Nome do Colaborador",
            height=50,
            hint_text="Digite parte do nome",
        )
        self.search_button = BotaoPadraoBuscar(
            tooltip="Buscar treinamentos",
            col={'xs':12, 'sm':3, 'md':2, 'lg':2, 'xl':2, 'xxl':2},
            height=50,
            icon=ft.Icons.SEARCH,
            icon_color=ft.Colors.GREY_900,
            on_click=lambda e: on_search_click(self.codigo_field.value, self.nome_field.value)
        )
        self.controls = [
            self.codigo_field,
            self.nome_field,
            self.search_button
        ]
