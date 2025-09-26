# recorder.py
import time
from pynput import mouse, keyboard

class MacroRecorder:
    def __init__(self):
        self.recorded_actions = []
        self.last_time = None
        self.is_recording = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

    def _record_action(self, action_type, **kwargs):
        """Função interna para registrar uma ação com seu delay."""
        if not self.is_recording:
            return

        current_time = time.time()
        delay = current_time - self.last_time if self.last_time else 0
        self.last_time = current_time

        action = {'action': action_type, 'delay': delay}
        action.update(kwargs)
        self.recorded_actions.append(action)

    # --- Funções de callback para os listeners ---
    def on_move(self, x, y):
        self._record_action('move', x=x, y=y)

    def on_click(self, x, y, button, pressed):
        action_type = 'click_press' if pressed else 'click_release'
        self._record_action(action_type, x=x, y=y, button=str(button))

    def on_scroll(self, x, y, dx, dy):
        self._record_action('scroll', x=x, y=y, dx=dx, dy=dy)

    def on_press(self, key):
        # Tecla de parada da gravação
        if key == keyboard.Key.esc:
            self.stop_recording()
            return False  # Para o listener do teclado

        try:
            self._record_action('key_press', key=key.char)
        except AttributeError:
            self._record_action('key_press', key=str(key))

    def on_release(self, key):
        try:
            self._record_action('key_release', key=key.char)
        except AttributeError:
            self._record_action('key_release', key=str(key))

    # --- Funções principais de controle ---
    def start_recording(self):
        """Inicia a gravação dos eventos."""
        self.recorded_actions = []
        self.last_time = time.time()
        self.is_recording = True

        # Inicia os listeners em threads separadas
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.mouse_listener.start()
        self.keyboard_listener.start()
        print("Gravação iniciada. Pressione 'Esc' para parar.")

    def stop_recording(self):
        """Para a gravação dos eventos."""
        if self.is_recording:
            self.is_recording = False
            if self.mouse_listener:
                self.mouse_listener.stop()
            if self.keyboard_listener:
                self.keyboard_listener.stop()
            print("Gravação parada.")
            return self.recorded_actions
        return []

    def play_recording(self, actions, stop_event):
        """
        Reproduz uma lista de ações gravadas.
        Verifica o 'stop_event' a cada passo para permitir o cancelamento.
        Retorna um status: 'OK', 'Cancelado' ou 'Erro'.
        """
        if not actions:
            print("Nenhuma ação para reproduzir.")
            return 'OK'

        print("Iniciando reprodução...")
        try:
            for action in actions:
                # Verifica se o evento de parada foi acionado pela thread principal
                if stop_event.is_set():
                    print("Reprodução cancelada pelo usuário.")
                    return 'Cancelado'

                time.sleep(action['delay'])

                action_type = action['action']

                if action_type == 'move':
                    self.mouse_controller.position = (action['x'], action['y'])
                elif action_type in ['click_press', 'click_release']:
                    self.mouse_controller.position = (action['x'], action['y'])
                    btn = mouse.Button.left if 'left' in action['button'] else mouse.Button.right
                    if action_type == 'click_press':
                        self.mouse_controller.press(btn)
                    else:
                        self.mouse_controller.release(btn)
                elif action_type == 'scroll':
                    self.mouse_controller.position = (action['x'], action['y'])
                    self.mouse_controller.scroll(action['dx'], action['dy'])
                elif action_type in ['key_press', 'key_release']:
                    key_str = action['key']
                    key = None
                    # Converte string de volta para objeto Key se necessário
                    if key_str.startswith('Key.'):
                        key = getattr(keyboard.Key, key_str.split('.')[-1])
                    else:
                        key = key_str

                    if action_type == 'key_press':
                        self.keyboard_controller.press(key)
                    else:
                        self.keyboard_controller.release(key)

        except Exception as e:
            print(f"Erro durante a reprodução: {e}")
            return 'Erro'

        print("Reprodução finalizada com sucesso.")
        return 'OK'