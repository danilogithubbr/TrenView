# D:\Projetos\TrenView\src\components\resultados_list.py

import flet as ft
from components.cartao_padrao import CartaoPadrao

class ResultadosList(ft.Column):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Texto de informação (número de resultados ou mensagens)
        self.info_text = ft.Text("", color=ft.Colors.BLACK)
        # Container para os cartões de resultados
        self.cards_column = ft.Column(spacing=5, run_spacing=5, scroll=ft.ScrollMode.AUTO, expand=True)
        # Inicialmente controles
        self.controls = [
            self.info_text,
            self.cards_column
        ]

    def clear(self):
        """Limpa os resultados exibidos e limpa o texto de info."""
        self.cards_column.controls.clear()
        self.info_text.value = ""
        self.update()

    def show_loading(self):
        """Exibe indicador de carregamento no lugar dos resultados."""
        self.clear()
        self.cards_column.controls.append(ft.ProgressRing())
        self.update()

    def show_results(self, resultados: list[dict]):
        """Exibe a lista de resultados (cada registro como CartaoPadrao)."""
        self.cards_column.controls.clear()
        for registro in resultados:
            card = CartaoPadrao(
                registro=registro,
                col={'xs':12, 'sm':10, 'md':8, 'lg':6, 'xl':4, 'xxl':2}
            )
            self.cards_column.controls.append(card)
        self.update()