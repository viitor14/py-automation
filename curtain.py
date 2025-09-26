# curtain.py
import customtkinter as ctk

class BlackCurtainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Esconde a janela principal inicial, pois só queremos o Toplevel
        self.withdraw()

        # Cria a janela da cortina como um Toplevel
        curtain_window = ctk.CTkToplevel(self)
        
        # Configurações da cortina
        width = curtain_window.winfo_screenwidth()
        height = curtain_window.winfo_screenheight()
        curtain_window.geometry(f"{width}x{height}+0+0")
        curtain_window.overrideredirect(True)
        curtain_window.attributes("-topmost", True)
        curtain_window.configure(fg_color="black")
        
        # Adiciona um texto para informar o usuário
        label = ctk.CTkLabel(curtain_window, 
                             text="Automação em execução, por favor aguarde...", 
                             font=ctk.CTkFont(size=22, weight="bold"), 
                             text_color="white")
        label.place(relx=0.5, rely=0.5, anchor="center")

        # Impede que a janela seja fechada pelo usuário
        curtain_window.protocol("WM_DELETE_WINDOW", lambda: None)

if __name__ == "__main__":
    app = BlackCurtainApp()
    app.mainloop()