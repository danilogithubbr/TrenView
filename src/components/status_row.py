# D:\Projetos\TrenView\src\components\status_row.py
import flet as ft

class StatusRow(ft.Row):
    def __init__(self, estado_ref: ft.Ref[ft.Text], **kwargs):
        super().__init__(**kwargs)
        #self.col = {'xs':12, 'sm':3, 'md':2, 'lg':2, 'xl':2, 'xxl':2},
        self.icon = ft.Icon(ft.Icons.STORAGE, color=ft.Colors.GREEN)
        self.text = ft.Text("Banco de Dados", ref=estado_ref)
        self.controls = [ self.icon, self.text ]