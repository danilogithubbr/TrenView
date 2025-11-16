from typing import Dict, Optional, Callable
import flet as ft
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR.parent / '.env')

class FileUpload(ft.Column):
    def __init__(
        self,
        upload_url: str,
        fixed_filename: str = "dados.csv",
        allowed_extensions: Optional[list] = None,
        on_upload_complete: Optional[Callable] = None
    ):
        super().__init__()
        self.upload_url = upload_url
        self.fixed_filename = fixed_filename
        self.allowed_extensions = allowed_extensions or ["csv"]
        self.on_upload_complete = on_upload_complete

        self.prog_bars: Dict[str, ft.ProgressRing] = {}
        self.upload_btn_ref = ft.Ref[ft.ElevatedButton]()
        self.file_picker_ref = ft.Ref[ft.FilePicker]()

        # Configura os controles iniciais da interface
        self.controls = [
            ft.ElevatedButton(
                "Selecione o arquivo...",
                icon=ft.Icons.FOLDER_OPEN,
                on_click=self._pick_files,
            ),
            ft.Column(),  # Coluna para exibir os arquivos
            ft.ElevatedButton(
                "Upload",
                ref=self.upload_btn_ref,
                icon=ft.Icons.UPLOAD,
                on_click=self._upload_files,
                disabled=True,
            ),
        ]
        
        # Referência para a coluna de arquivos
        self.files_ref = self.controls[1]

    def _pick_files(self, e):
        self.file_picker_ref.current.pick_files(
            allow_multiple=False,
            allowed_extensions=self.allowed_extensions
        )

    def _file_picker_result(self, e: ft.FilePickerResultEvent):
        self.upload_btn_ref.current.disabled = True if e.files is None else False
        self.prog_bars.clear()
        self.files_ref.controls.clear()

        if e.files is not None:
            for f in e.files:
                # VERIFICAÇÃO DE ARQUIVO CSV - ADICIONADA AQUI
                if f.name.endswith('.csv'):
                    prog = ft.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                    self.prog_bars[self.fixed_filename] = prog
                    self.files_ref.controls.append(
                        ft.Row([prog, ft.Text(f.name)])
                    )
                else:
                    # MOSTRAR MENSAGEM DE ERRO PARA ARQUIVOS NÃO CSV
                    self.page.add(
                        ft.SnackBar(
                            ft.Text("Apenas arquivos .csv são permitidos!"),
                            open=True
                        )
                    )
        self.update()

    def _on_upload_progress(self, e: ft.FilePickerUploadEvent):
        if self.fixed_filename in self.prog_bars:
            self.prog_bars[self.fixed_filename].value = e.progress
            self.prog_bars[self.fixed_filename].update()

    def _upload_files(self, e):
        if not self.file_picker_ref.current.result:
            return
            
        if self.file_picker_ref.current.result.files is None:
            return

        upload_files = []
        for f in self.file_picker_ref.current.result.files:
            upload_files.append(
                ft.FilePickerUploadFile(
                    f.name,
                    upload_url=self.upload_url,
                )
            )
        self.file_picker_ref.current.upload(upload_files)
        
        # Chamar callback quando o upload for concluído
        if self.on_upload_complete:
            self.on_upload_complete()

    def did_mount(self):
        # Cria e adiciona o FilePicker à overlay após montagem
        file_picker = ft.FilePicker(
            ref=self.file_picker_ref,
            on_result=self._file_picker_result,
            on_upload=self._on_upload_progress,
        )
        self.page.overlay.append(file_picker)
        self.page.update()

    def will_unmount(self):
        # Remove o FilePicker da overlay ao desmontar
        if self.file_picker_ref.current in self.page.overlay:
            self.page.overlay.remove(self.file_picker_ref.current)
            self.page.update()