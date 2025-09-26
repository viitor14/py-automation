# run_macro.py
import time
import os
import json # Importação necessária
from recorder import MacroRecorder
from network_checker import check_internet
from logger_setup import app_logger

# --- CONFIGURAÇÃO AUTOMÁTICA ---
# O script agora busca o arquivo de macro automaticamente na pasta %APPDATA%
APP_DATA_FOLDER = os.path.join(os.getenv('APPDATA'), 'PyAutomacaoMacro')
MACRO_FILE_PATH = os.path.join(APP_DATA_FOLDER, 'macro.json')
# -----------------------------

def main():
    """
    Função principal que carrega e executa a macro.
    """
    print("Iniciando executor de macro...")
    app_logger.info("Executor de macro iniciado.")

    # Verifica se o arquivo de macro existe
    if not os.path.exists(MACRO_FILE_PATH):
        print(f"Erro: Arquivo de macro '{MACRO_FILE_PATH}' não encontrado.")
        app_logger.error(f"Arquivo de macro '{MACRO_FILE_PATH}' não encontrado.")
        return

    # Loop de espera pela internet
    if not check_internet():
        print("Aguardando conexão com a internet...")
        app_logger.info("Sem internet, aguardando conexão...")
        while not check_internet():
            time.sleep(5)
    
    print("Internet detectada. Carregando e executando a macro...")
    app_logger.info("Internet detectada. Iniciando a macro.")

    # Carrega as ações do arquivo JSON
    try:
        with open(MACRO_FILE_PATH, 'r') as f:
            actions_to_play = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar o arquivo de macro: {e}")
        app_logger.error(f"Erro ao carregar o arquivo de macro: {e}")
        return

    if actions_to_play:
        reproducer = MacroRecorder()
        reproducer.play_recording(actions_to_play)
        app_logger.info(f"Macro '{MACRO_FILE_PATH}' executada com sucesso.")
    else:
        print("Nenhuma ação encontrada na macro.")
        app_logger.warning("Nenhuma ação encontrada na macro.")

    print("Automação finalizada.")

if __name__ == "__main__":
    time.sleep(10) 
    main()