# run_macro.py
import time
import os
import json
import subprocess
import sys
from recorder import MacroRecorder
from network_checker import check_internet
from logger_setup import app_logger

# --- CONFIGURAÇÃO AUTOMÁTICA ---
APP_DATA_FOLDER = os.path.join(os.getenv('APPDATA'), 'PyAutomacaoMacro')
MACRO_FILE_PATH = os.path.join(APP_DATA_FOLDER, 'macro.json')
# -----------------------------

def main():
    print("Iniciando executor de macro...")
    app_logger.info("Executor de macro iniciado.")

    # --- LÓGICA DA CORTINA ---
    curtain_process = None
    try:
        # Encontra o executável pythonw.exe no venv para rodar a cortina sem console
        pythonw_exe = os.path.join(sys.prefix, 'pythonw.exe')
        if not os.path.exists(pythonw_exe):
            # Fallback para python.exe se pythonw.exe não for encontrado
            pythonw_exe = os.path.join(sys.prefix, 'Scripts', 'pythonw.exe')
            if not os.path.exists(pythonw_exe):
                 pythonw_exe = os.path.join(sys.prefix, 'python.exe')


        curtain_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'curtain.py')
        
        print("Lançando cortina visual...")
        # Inicia o processo da cortina em segundo plano
        curtain_process = subprocess.Popen([pythonw_exe, curtain_script_path])
        # Dá um pequeno tempo para a janela da cortina aparecer
        time.sleep(2)
        # -------------------------

        if not os.path.exists(MACRO_FILE_PATH):
            print(f"Erro: Arquivo de macro '{MACRO_FILE_PATH}' não encontrado.")
            app_logger.error(f"Arquivo de macro '{MACRO_FILE_PATH}' não encontrado.")
            return

        if not check_internet():
            print("Aguardando conexão com a internet...")
            app_logger.info("Sem internet, aguardando conexão...")
            while not check_internet():
                time.sleep(5)
        
        print("Internet detectada. Carregando e executando a macro...")
        app_logger.info("Internet detectada. Iniciando a macro.")

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

    finally:
        # --- LÓGICA DE FINALIZAÇÃO DA CORTINA ---
        # Este bloco SEMPRE será executado, mesmo se ocorrer um erro na macro.
        if curtain_process:
            print("Fechando cortina visual...")
            curtain_process.terminate() # Encerra o processo da cortina
        # ------------------------------------
        print("Automação finalizada.")


if __name__ == "__main__":
    time.sleep(5) # Delay inicial um pouco menor
    main()