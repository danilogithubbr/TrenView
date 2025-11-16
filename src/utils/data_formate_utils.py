# D:\Projetos\TrenView\src\utils\data_formate_utils.py
from datetime import datetime, date, timedelta
import flet as ft
from typing import Union

def formatar_data_brasileira(data: Union[datetime, date, str]) -> str:
    """
    Converte uma data/hora para o formato brasileiro.
    
    Args:
        data: Pode ser datetime, date ou string em formato ISO
        
    Returns:
        str: Data formatada no padrão brasileiro DD/MM/AAAA HH:MM:SS
    """
    try:
        # Se for string, converter para datetime primeiro
        if isinstance(data, str):
            # Tenta converter de formato ISO
            if 'T' in data:
                data_obj = datetime.fromisoformat(data.replace('Z', '+00:00'))
            else:
                # Tenta outros formatos comuns
                try:
                    data_obj = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    try:
                        data_obj = datetime.strptime(data, '%Y-%m-%d')
                    except ValueError:
                        # Última tentativa com formato date
                        data_obj = datetime.strptime(data, '%Y-%m-%d')
        
        # Se já for datetime
        elif isinstance(data, datetime):
            data_obj = data
        
        # Se for date (sem hora)
        elif isinstance(data, date):
            data_obj = datetime.combine(data, datetime.min.time())
        
        else:
            raise ValueError(f"Tipo de data não suportado: {type(data)}")
        
        # Formatar para padrão brasileiro
        if data_obj.time() == datetime.min.time():
            # Se não tem hora (é meia-noite), mostrar apenas data
            return data_obj.strftime('%d/%m/%Y')
        else:
            # Se tem hora, mostrar data e hora
            return data_obj.strftime('%d/%m/%Y %H:%M:%S')
            
    except Exception as e:
        # Em caso de erro, retorna string original ou mensagem de erro
        return str(data) if data else "Data inválida"
    

def formatar_status_vencimento(registro):
    """
    Formata o status e data de vencimento com cores conforme as regras:
    - Vermelho: data vencida, muito antiga (>10 anos) ou muito futura (>10 anos)
    - Verde: data dentro do período normal
    """
    status = registro.get('Status', 'N/A')
    data_vencimento = registro.get('DataVencimento')
    hoje = date.today()
    
    # Se não há data de vencimento, mostra apenas o status em vermelho
    if not data_vencimento:
        return ft.Text(f"{status}", color=ft.Colors.RED)
    
    # Converte para objeto date se for string
    if isinstance(data_vencimento, str):
        try:
            data_vencimento = datetime.strptime(data_vencimento, '%Y-%m-%d').date()
        except ValueError:
            return ft.Text(f"{status}", color=ft.Colors.RED)
    
    # Calcula limites de 10 anos
    dez_anos_atras = hoje - timedelta(days=365*10)
    dez_anos_frente = hoje + timedelta(days=365*10)
    
    # Condição 1: Data vencida (menor que hoje)
    if data_vencimento < hoje and data_vencimento >= dez_anos_atras:
        return ft.Text(
            f"{status} em {formatar_data_brasileira(data_vencimento)}", color=ft.Colors.RED
        )
    
    # Condição 2: Data muito antiga (>10 anos atrás)
    if data_vencimento < dez_anos_atras:
        return ft.Text(f"{status}", color=ft.Colors.RED)
    
    # Condição 3: Data muito futura (>10 anos à frente)
    if data_vencimento > dez_anos_frente:
        return ft.Text(f"{status}", color=ft.Colors.GREEN)
    
    # Condição 4: Data normal (mostra data completa em verde)
    return ft.Text(
        f"{status} em {formatar_data_brasileira(data_vencimento)}",
        color=ft.Colors.GREEN
    )

# Função para converter data do Excel para datetime
def converter_data_excel(data_excel):
    try:
        # Se já for uma string de data, retornar como está
        if isinstance(data_excel, str):
            # Tentar converter de string para datetime
            try:
                return datetime.strptime(data_excel, '%Y-%m-%d').strftime('%Y-%m-%d')
            except:
                try:
                    return datetime.strptime(data_excel, '%d/%m/%Y').strftime('%Y-%m-%d')
                except:
                    try:
                        return datetime.strptime(data_excel, '%m/%d/%Y').strftime('%Y-%m-%d')
                    except:
                        return data_excel  # Retornar original se não conseguir converter
        
        # Se for número (formato Excel), converter
        if isinstance(data_excel, (int, float)):
            # Data base do Excel é 1 de janeiro de 1900
            data_base = datetime(1900, 1, 1)
            # Ajuste para o bug do Excel que considera 1900 como ano bissexto
            if data_excel > 60:
                data_excel -= 1
            data_calculada = data_base + timedelta(days=data_excel - 1)
            return data_calculada.strftime('%Y-%m-%d')
        
        return data_excel  # Retornar original se não for string nem número
    except:
        return data_excel  # Retornar original em caso de erro