# D:\Projetos\TrenView\src\pages\home.py
from datetime import datetime
import flet as ft
from components.file_upload import FileUpload
from components.search_form import SearchForm
from components.resultados_list import ResultadosList
from components.status_row import StatusRow
from services.busca_service import buscar_treinamentos, estatisticas_banco
from utils.data_formate_utils import formatar_data_brasileira
from models.database import csv_para_json


def home_page(page: ft.Page):
    # configuração da página
    page.title = "Consulta de Treinamentos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = ft.padding.only(left=10, right=10)
    #page.scroll = ft.ScrollMode.ADAPTIVE

    # referências de estado
    estado_dados = ft.Ref[ft.Text]()
    info_text = ft.Ref[ft.Text]()

    def handle_upload_complete():
        csv_para_json("uploads/dados.csv")
        page.add(ft.SnackBar(ft.Text("Upload concluído com sucesso!"), open=True))
        page.update()

    # componentes reutilizáveis
    upload_component = FileUpload(
        upload_url=page.get_upload_url("dados.csv", 60),
        fixed_filename="dados.csv",
        allowed_extensions=["csv"],
        on_upload_complete=handle_upload_complete
    )
    status_row = StatusRow(estado_ref=estado_dados)
    search_form = SearchForm(on_search_click=lambda codigo, nome: on_search_click(codigo, nome))
    resultados_list = ResultadosList()

    def atualizar_status():
        try:
            stats = estatisticas_banco()
            ultima = stats["ultima_importacao"]
            # Se não houve importação ainda
            if ultima == "Nunca" or not ultima:
                data_formatada = "Nunca"
            else:
                # Converte string ISO para datetime
                try:
                    dt = datetime.fromisoformat(ultima)
                    data_formatada = formatar_data_brasileira(dt)
                except Exception:
                    # Se der erro no parse, mostra o texto original
                    data_formatada = ultima

            estado_dados.current.value = (
                f"Atualizado em {data_formatada} - "
                f"{stats['total_registros']} registros - "
                f"{stats['tamanho_banco']}"
            )
            estado_dados.current.color = ft.Colors.GREEN

        except Exception as e:
            estado_dados.current.value = f"❌ Erro no banco: {str(e)}"
            estado_dados.current.color = ft.Colors.RED

        page.update()

    
    def on_search_click(codigo: str, nome: str):
        resultados_list.clear()
        if not codigo and not nome:
            info_text.current.value = "Por favor, informe código ou nome para busca."
            info_text.current.color = ft.Colors.ORANGE
            page.update()
            return

        resultados_list.show_loading()
        page.update()

        try:
            resultados = buscar_treinamentos(codigo=codigo, nome=nome, limite=50)
            resultados_list.show_results(resultados)
            info_text.current.value = f"Encontrados {len(resultados)} resultados"
            info_text.current.color = ft.Colors.GREEN
        except Exception as ex:
            resultados_list.clear()
            info_text.current.value = f"❌ Erro na busca: {str(ex)}"
            info_text.current.color = ft.Colors.RED

        page.update()

    #layout
    page.add(
       
        # Container superior (não expansível)
        ft.ExpansionTile(
            title=ft.Text("Administração", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
            controls=[
                ft.ResponsiveRow(
                    run_spacing=5,
                    spacing=10,
                    expand=True,
                    controls=[upload_component],
                )
            ],
            initially_expanded=False,
            controls_padding=ft.padding.only(right=15)
        ),
        
        # Container de resultados (expansível)
        ft.ExpansionTile(
            title=ft.Text("Consulta:", theme_style=ft.TextThemeStyle.TITLE_SMALL),
            subtitle=ft.Text(ref=info_text),
            controls=[
                ft.Container(content=search_form, padding=ft.padding.only(top=3)),
                ft.GridView(
                    controls=[resultados_list],
                    runs_count=1,
                    height=1000,
                ),
            ],
            initially_expanded=True,
            #expand=True,
            controls_padding=ft.padding.only(right=15)
        ),

    )

    # status inicial
    atualizar_status()