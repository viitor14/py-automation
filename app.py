# app.py
import customtkinter as ctk
import threading
from recorder import MacroRecorder
from file_handler import save_actions, load_actions

class MacroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Py Automação - Macro Recorder")
        self.geometry("400x250")
        
        # Aparência
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Instância do gravador
        self.recorder = MacroRecorder()
        self.is_recording_state = False

        # --- Widgets ---
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

    def toggle_recording(self):
        """Inicia ou para a gravação."""
        if not self.is_recording_state:
            # Iniciar gravação
            self.is_recording_state = True
            self.record_button.configure(text="Parar Gravação (Pressione ESC)")
            self.play_button.configure(state="disabled")
            self.status_label.configure(text="Gravando... Pressione ESC para parar.")
            
            # Executa a gravação em uma thread para não travar a GUI
            threading.Thread(target=self.recorder.start_recording, daemon=True).start()
        else:
            # O ESC já para a gravação, mas este botão pode ser um backup
            # A lógica principal de parada está no on_press (ESC) em recorder.py
            # Aqui, apenas redefinimos a interface.
            self.handle_recording_stop()

    def handle_recording_stop(self):
        """Chamado quando a gravação é interrompida (via ESC)."""
        if self.is_recording_state:
            self.is_recording_state = False
            recorded_actions = self.recorder.recorded_actions
            
            self.record_button.configure(text="Iniciar Gravação")
            self.play_button.configure(state="normal")
            
            if recorded_actions:
                self.status_label.configure(text=f"{len(recorded_actions)} ações gravadas. Salvando...")
                # Salva as ações e atualiza o status
                if save_actions(recorded_actions):
                    self.status_label.configure(text="Gravação salva com sucesso!")
                else:
                    self.status_label.configure(text="Salvamento cancelado.")
            else:
                self.status_label.configure(text="Gravação finalizada sem ações.")

    def play_macro(self):
        """Carrega e reproduz um arquivo de macro."""
        actions_to_play = load_actions()
        
        if actions_to_play:
            self.status_label.configure(text="Reproduzindo... A aplicação ficará travada.")
            self.record_button.configure(state="disabled")
            self.play_button.configure(state="disabled")
            
            # Define uma função para rodar na thread
            def playback_thread():
                self.recorder.play_recording(actions_to_play)
                # Quando terminar, reabilita os botões na thread principal
                self.after(0, self.on_playback_finished)
            
            # Inicia a reprodução em uma nova thread para não congelar a GUI
            threading.Thread(target=playback_thread, daemon=True).start()

    def on_playback_finished(self):
        """Reabilita a interface após a reprodução."""
        self.status_label.configure(text="Reprodução finalizada. Pronto.")
        self.record_button.configure(state="normal")
        self.play_button.configure(state="normal")
        
    def check_recorder_status(self):
        """Verifica periodicamente se a gravação foi parada pela tecla ESC."""
        if self.is_recording_state and not self.recorder.is_recording:
            self.handle_recording_stop()
        self.after(100, self.check_recorder_status)


if __name__ == "__main__":
    app = MacroApp()
    app.check_recorder_status() # Inicia o loop de verificação
    app.mainloop()