# file_handler.py
import json
import os

# Define o caminho padrão para salvar os dados do aplicativo
# os.getenv('APPDATA') é a forma correta de obter a pasta %APPDATA% no Windows
APP_DATA_FOLDER = os.path.join(os.getenv('APPDATA'), 'PyAutomacaoMacro')
MACRO_FILE_PATH = os.path.join(APP_DATA_FOLDER, 'macro.json')

def save_actions_automatically(actions):
    """
    Salva as ações automaticamente em um local e nome de arquivo fixos.
    Substitui qualquer arquivo existente.
    """
    if not actions:
        print("Nenhuma ação para salvar.")
        return False
    
    try:
        # Garante que a pasta de destino exista. Se não, cria.
        os.makedirs(APP_DATA_FOLDER, exist_ok=True)

        # Salva o arquivo, sobrescrevendo se já existir (modo 'w')
        with open(MACRO_FILE_PATH, 'w') as f:
            json.dump(actions, f, indent=4)
        
        print(f"Gravação salva com sucesso em: {MACRO_FILE_PATH}")
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo automaticamente: {e}")
        return False

def load_actions_automatically():
    """
    Carrega as ações do local e nome de arquivo fixos.
    """
    try:
        # Verifica se o arquivo de macro existe no local esperado
        if not os.path.exists(MACRO_FILE_PATH):
            print(f"Arquivo de macro não encontrado em {MACRO_FILE_PATH}. Grave uma macro primeiro.")
            return None

        # Carrega as ações do arquivo
        with open(MACRO_FILE_PATH, 'r') as f:
            actions = json.load(f)
        
        print(f"Gravação carregada de: {MACRO_FILE_PATH}")
        return actions
    except Exception as e:
        print(f"Erro ao carregar o arquivo automaticamente: {e}")
        return None