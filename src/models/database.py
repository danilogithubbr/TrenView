import os
import pandas as pd 
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from utils.data_formate_utils import converter_data_excel

# Caminho para o arquivo JSON
ASSETS_DIR = "assets"
JSON_PATH = os.path.join(ASSETS_DIR, "treinamentos.json")

# Função para salvar JSON (ESCOPO GLOBAL)
def salvar_json(dados):
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    ts_path = os.path.join(ASSETS_DIR, "last_importacao.txt")
    # grava em ISO format (ex: 2025-11-16T08:12:34+00:00) — fácil de ler e parsear
    now_iso = datetime.now().astimezone().isoformat()
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write(now_iso)

# Função para converter CSV para JSON (ESCOPO GLOBAL)
def csv_para_json(file_path, password=None, file_name=None):
    try:
        # Tentar diferentes configurações para ler o CSV
        try:
            # Primeira tentativa: leitura padrão
            df = pd.read_csv(file_path)
        except pd.errors.ParserError:
            try:
                # Segunda tentativa: usar ponto e vírgula como delimitador
                df = pd.read_csv(file_path, sep=';')
            except pd.errors.ParserError:
                try:
                    # Terceira tentativa: usar tab como delimitador
                    df = pd.read_csv(file_path, sep='\t')
                except:
                    # Quarta tentativa: detectar delimitador automaticamente
                    df = pd.read_csv(file_path, sep=None, engine='python')
        
        # Verificar colunas necessárias
        colunas_necessarias = ['Controle', 'Nome do Colaborador', 'Treinamento', 
                             'Descricao Treinamento', 'DataVencimento', 'Status']
        
        # Verificar se todas as colunas necessárias estão presentes
        colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]
        if colunas_faltantes:
            # Tentar encontrar colunas com nomes similares (case insensitive)
            df.columns = df.columns.str.strip().str.lower()
            colunas_necessarias_lower = [col.lower() for col in colunas_necessarias]
            
            colunas_faltantes_lower = [col for col in colunas_necessarias_lower if col not in df.columns]
            if colunas_faltantes_lower:
                return False, f"CSV não contém todas as colunas necessárias! Faltando: {', '.join(colunas_faltantes)}"
            
            # Mapear colunas para os nomes corretos
            mapeamento_colunas = {}
            for col_necessaria in colunas_necessarias:
                for col_csv in df.columns:
                    if col_necessaria.lower() == col_csv.lower():
                        mapeamento_colunas[col_necessaria] = col_csv
                        break
            
            # Renomear colunas
            df = df.rename(columns=mapeamento_colunas)
        
        # Selecionar apenas as colunas necessárias
        df = df[colunas_necessarias]
        
        # Converter datas do formato Excel para datetime
        if 'DataVencimento' in df.columns:
            df['DataVencimento'] = df['DataVencimento'].apply(converter_data_excel)
        
        # Limpar dados - remover linhas com valores NaN em colunas importantes
        df = df.dropna(subset=['Nome do Colaborador', 'Treinamento'])
        
        # Converter para dicionário
        dados = df.to_dict('records')
        
        # Salvar JSON
        salvar_json(dados)
        
        return True, f"CSV convertido com sucesso! {len(dados)} registros importados."
        
    except Exception as e:
        print(f"Erro ao processar CSV: {str(e)}")
        return False, f"Erro ao processar CSV: {str(e)}"


    """Obtém estatísticas do arquivo JSON."""
    try:
        if not JSON_PATH.exists():
            return {
                "total_registros": 0,
                "ultima_importacao": "Nunca",
                "tamanho_banco": "Arquivo não encontrado"
            }
        
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            registros = json.load(f)
        
        # Encontrar última importação
        ultima_importacao = None
        for registro in registros:
            data_import = registro.get('data_importacao')
            if data_import:
                if not ultima_importacao or data_import > ultima_importacao:
                    ultima_importacao = data_import
        
        # Calcular tamanho do arquivo
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
    except Exception as e:
        return {
            "total_registros": 0,
            "ultima_importacao": "Erro",
            "tamanho_banco": f"Erro: {str(e)}"
        }