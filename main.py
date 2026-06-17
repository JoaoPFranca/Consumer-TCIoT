"""
Entrada do sistema. Carrega ambiente e inicia o monitoramento.
"""
import logging
import signal
import sys
from dotenv import load_dotenv
from subscriber import Subscriber
from alerts.manager import AlertManager

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def encerrar(sig, frame):
    logger.info("Sistema encerrado.")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, encerrar)
    logger.info("Iniciando monitoramento IoT...")
    
    try:
        alert_manager = AlertManager()
        sub = Subscriber(alert_manager)
        sub.iniciar()
    except Exception as e:
        logger.critical(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
