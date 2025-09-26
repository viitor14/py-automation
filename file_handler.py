# file_handler.py
import json
import tkinter as tk
from tkinter import filedialog

def save_actions(actions):
    """
    Abre uma janela para o usuário escolher onde salvar o arquivo JSON
    e salva as ações gravadas.
    Retorna True se salvou com sucesso, False caso contrário.
    """
    if not actions:
        print("Nenhuma ação para salvar.")
        return False

    # Esconde a janela raiz do Tkinter
    root = tk.Tk()
    root.withdraw()

    # Pede ao usuário para escolher o local e o nome do arquivo
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Salvar gravação como..."
    )

    if file_path:
        try:
            with open(file_path, 'w') as f:
                json.dump(actions, f, indent=4)
            print(f"Gravação salva com sucesso em: {file_path}")
            return True
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")
            return False
    else:
        print("Operação de salvar cancelada.")
        return False

def load_actions():
    """
    Abre uma janela para o usuário escolher um arquivo JSON para carregar.
    Retorna a lista de ações ou None se a operação for cancelada ou falhar.
    """
    # Esconde a janela raiz do Tkinter
    root = tk.Tk()
    root.withdraw()

    # Pede ao usuário para escolher um arquivo
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Abrir gravação..."
    )

    if file_path:
        try:
            with open(file_path, 'r') as f:
                actions = json.load(f)
            print(f"Gravação carregada de: {file_path}")
            return actions
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            return None
    else:
        print("Operação de carregar cancelada.")
        return None