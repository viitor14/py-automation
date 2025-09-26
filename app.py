# app.py
import customtkinter as ctk
import threading
import time
from recorder import MacroRecorder
from file_handler import save_actions, load_actions
from logger_setup import app_logger
from network_checker import check_internet

class MacroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Py Automação - Macro Recorder")
        self.geometry("400x300")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.recorder = MacroRecorder()
        self.is_recording_state = False
        self.playback_window = None
        self.stop_playback_event = threading.Event()
        self.cancel_wait_event = threading.Event()

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Gravador de Macro", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=12, padx=10)
        
        self.status_label = ctk.CTkLabel(self.main_frame, text="Pronto para começar.", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=10)

        self.record_button = ctk.CTkButton(self.main_frame, text="Iniciar Gravação", command=self.toggle_recording)
        self.record_button.pack(pady=10, fill="x", padx=30)
        
        self.play_button = ctk.CTkButton(self.main_frame, text="Reproduzir Gravação", command=self.play_macro)
        self.play_button.pack(pady=10, fill="x", padx=30)

    def play_macro(self):
        actions_to_play = load_actions()
        if not actions_to_play:
            return

        self.record_button.configure(state="disabled")
        self.play_button.configure(state="disabled")
        
        if check_internet():
            self._start_playback_logic(actions_to_play)
        else:
            app_logger.info("Tentativa de reprodução — Sem internet — aguardando conexão...")
            self.status_label.configure(text="Sem internet. Aguardando conexão...")
            self.cancel_wait_event.clear()
            self.show_wait_for_internet_window()
            wait_thread = threading.Thread(target=self._internet_waiter_thread, args=(actions_to_play,), daemon=True)
            wait_thread.start()

    def _internet_waiter_thread(self, actions):
        while not self.cancel_wait_event.is_set():
            if check_internet():
                app_logger.info("Internet detectada — Macro iniciada")
                self.after(0, self._start_playback_logic, actions)
                return
            # Comente ou altere o valor abaixo para mudar o intervalo de verificação
            time.sleep(5)

    def _start_playback_logic(self, actions):
        if self.playback_window:
            self.playback_window.destroy()
            self.playback_window = None
        self.status_label.configure(text="Reproduzindo...")
        
        def playback_thread_worker():
            self.recorder.play_recording(actions)
            self.after(0, self.on_playback_finished)
        
        threading.Thread(target=playback_thread_worker, daemon=True).start()

    def show_wait_for_internet_window(self):
        self.playback_window = ctk.CTkToplevel(self)
        self.playback_window.title("Aguardando Conexão")
        self.playback_window.geometry("400x150")
        self.playback_window.transient(self); self.playback_window.grab_set()
        self.playback_window.protocol("WM_DELETE_WINDOW", self.cancel_wait_and_play)
        self.playback_window.resizable(False, False)
        progress_label = ctk.CTkLabel(self.playback_window, text="Aguardando conexão com a internet\npara iniciar a automação...", 
                                      font=ctk.CTkFont(size=14), justify="center")
        progress_label.pack(pady=20, padx=20, expand=True)
        cancel_button = ctk.CTkButton(self.playback_window, text="Cancelar", command=self.cancel_wait_and_play, 
                                      fg_color="red", hover_color="#C00000")
        cancel_button.pack(pady=10)

    def cancel_wait_and_play(self):
        app_logger.info("Reprodução cancelada pelo usuário antes da conexão")
        self.cancel_wait_event.set()
        if self.playback_window:
            self.playback_window.destroy()
            self.playback_window = None
        self.on_playback_finished(was_cancelled=True)

    def on_playback_finished(self, was_cancelled=False):
        if not was_cancelled:
            app_logger.info("Reprodução concluída com sucesso")
            self.status_label.configure(text="Reprodução finalizada. Pronto.")
        else:
            self.status_label.configure(text="Operação cancelada pelo usuário.")
        self.record_button.configure(state="normal")
        self.play_button.configure(state="normal")

    def toggle_recording(self):
        if not self.is_recording_state:
            self.is_recording_state = True
            self.recorder.recorded_actions = []
            self.record_button.configure(text="Parar Gravação (Pressione ESC)")
            self.play_button.configure(state="disabled")
            self.status_label.configure(text="Gravando... Pressione ESC para parar.")
            threading.Thread(target=self.recorder.start_recording, daemon=True).start()
        else:
            self.handle_recording_stop()

    def handle_recording_stop(self):
        if self.is_recording_state:
            self.is_recording_state = False
            recorded_actions = self.recorder.recorded_actions
            self.record_button.configure(text="Iniciar Gravação")
            self.play_button.configure(state="normal")
            if recorded_actions:
                self.status_label.configure(text=f"{len(recorded_actions)} ações gravadas. Salvando...")
                if save_actions(recorded_actions): self.status_label.configure(text="Gravação salva com sucesso!")
                else: self.status_label.configure(text="Salvamento cancelado.")
            else: self.status_label.configure(text="Gravação finalizada sem ações.")
    
    def check_recorder_status(self):
        if self.is_recording_state and not self.recorder.is_recording:
            self.handle_recording_stop()
        self.after(100, self.check_recorder_status)

if __name__ == "__main__":
    app = MacroApp()
    app.check_recorder_status()
    app.mainloop()