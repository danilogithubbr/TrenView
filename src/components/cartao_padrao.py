# D:\Projetos\TrenView\src\components\cartao_padrao.py
import flet as ft
from utils.data_formate_utils import formatar_data_brasileira, formatar_status_vencimento

class CartaoPadrao(ft.Card):
    def __init__(self, registro: dict, **kwargs):
        super().__init__(**kwargs)
        # aqui seus estilos fixos ou customizáveis
        self.color = ft.Colors.GREY_100
        self.elevation = 5
        self.shadow_color = ft.Colors.BLUE_900
        self.margin = ft.margin.all(1)
        self.expand = True

        # conteúdo interno
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        spans=[
                            ft.TextSpan(text=f"{registro.get('Controle', 'N/A')}: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                            ft.TextSpan(text=f"{registro.get('Nome do Colaborador', 'N/A')}"),
                        ]),
                    ft.Text(
                        spans=[
                            ft.TextSpan(text=f"{registro.get('Treinamento', 'N/A')}: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                            ft.TextSpan(text=f"{registro.get('Descricao Treinamento', 'N/A')}"),
                        ]),
                    #ft.Text(f"{registro.get('treinamento', 'N/A')}: {registro.get('descricao', 'N/A')}"),
                    #ft.Text(f"{registro.get('status', 'N/A')} em {formatar_data_brasileira(registro.get('data_vencimento', 'N/A'))}"),
                    formatar_status_vencimento(registro)
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                run_spacing=5
            ),
            padding=10,
            expand=True,
            alignment=ft.alignment.center,
            margin=ft.margin.symmetric(vertical=0, horizontal=5),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.WHITE, ft.Colors.BLUE_50]
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                color=ft.Colors.BLUE_200,
                blur_radius=5,
                offset=ft.Offset(x=2, y=2)
            ),
            border=ft.border.only(
                left=ft.BorderSide(width=5, color=ft.Colors.BLUE),
                right=ft.BorderSide(width=5, color=ft.Colors.BLUE)
            ),
            border_radius=ft.border_radius.only(
                top_left=10, top_right=10, bottom_left=10, bottom_right=10
            ),
        )

        # você também pode permitir customização de col (coluna responsiva) via **kwargs
        if 'col' in kwargs:
            self.col = kwargs.pop('col')