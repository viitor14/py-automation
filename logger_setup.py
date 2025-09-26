# logger_setup.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Configura e retorna um logger para registrar as execuções."""
    # Cria o logger
    logger = logging.getLogger('MacroReplayLogger')
    logger.setLevel(logging.INFO)

    # Evita adicionar handlers duplicados se a função for chamada mais de uma vez
    if logger.hasHandlers():
        logger.handlers.clear()

    # Cria um handler que rotaciona o arquivo de log para não ficar muito grande
    handler = RotatingFileHandler(
        'replays.log', maxBytes=5*1024*1024, backupCount=2
    )

    # Define o formato da mensagem de log
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    # Adiciona o handler ao logger
    logger.addHandler(handler)

    return logger

# Cria uma instância global do logger para ser importada por outros módulos
app_logger = setup_logger()