import json
from pathlib import Path
import os
from typing import List, Dict, Optional

# Caminho para o arquivo JSON
BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "assets" / "treinamentos.json"

def carregar_treinamentos() -> List[Dict]:
    """Carrega os dados do arquivo JSON."""
    try:
        
        if JSON_PATH.exists():
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Erro ao carregar arquivo JSON: {e}")
        return []

def buscar_treinamentos(codigo: str = None, nome: str = None, limite: int = 100) -> List[Dict]:
    """Busca treinamentos no arquivo JSON com filtros opcionais."""
    registros = carregar_treinamentos()
    resultados = []
        
    for registro in registros:
        # Aplicar filtros
        match_codigo = True
        match_nome = True
        
        if codigo:
            codigo_registro = str(registro.get('Controle', ''))
            match_codigo = codigo.lower() in codigo_registro.lower()
        if nome:
            match_nome = nome.lower() in registro.get('Nome do Colaborador', '').lower()
        
        if match_codigo and match_nome:
            resultados.append(registro)
        
        # Limitar resultados
        if len(resultados) >= limite:
            break
    
    return resultados

def estatisticas_banco() -> Dict:
    """Obtém estatísticas do arquivo JSON."""
    registros = carregar_treinamentos()
    
    # Encontrar data da última importação — agora vindas do arquivo em assets/last_importacao.txt
    ultima_importacao = None
    #uploads_dir = os.path.join("assets", "last_importacao.txt")
    assets_dir = "assets"
    file_name = "last_importacao.txt"
    ts_path = Path(assets_dir) / file_name

    if ts_path.exists():
        try:
            conteudo = ts_path.read_text(encoding='utf-8').strip()
            # retornamos a string tal como foi salva (ISO). Se quiser podemos parsear para datetime.
            ultima_importacao = conteudo if conteudo else None
        except Exception:
            ultima_importacao = None
    else:
        ultima_importacao = None
    
    # Calcular tamanho do arquivo
    tamanho_arquivo = "Arquivo não encontrado"
    if JSON_PATH.exists():
        size = JSON_PATH.stat().st_size
        if size > 1024 * 1024:
            tamanho_arquivo = f"{size / (1024 * 1024):.2f} MB"
        elif size > 1024:
            tamanho_arquivo = f"{size / 1024:.2f} KB"
        else:
            tamanho_arquivo = f"{size} bytes"
    
    return {
        "total_registros": len(registros),
        "ultima_importacao": ultima_importacao or "Nunca",
        "tamanho_banco": tamanho_arquivo
    }

