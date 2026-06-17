"""
Publicador (Publisher) - Simulador de Sensor para PC.
Este script simula um dispositivo IoT (como ESP32 com DHT22) enviando dados via MQTT.
Utilizado como ambiente de teste e salva-guarda para o sistema de monitoramento.
"""
import paho.mqtt.client as mqtt
import json
import time
import random
import logging
import sys
from datetime import datetime
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, INTERVALO_ENVIO

# Configuracao de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def gerar_dados_simulados():
    """
    Simula um sensor DHT22 gerando temperatura e umidade.
    """
    temperatura = round(random.uniform(22.0, 33.0), 1)
    umidade = round(random.uniform(40.0, 65.0), 1)
    
    return {
        "temperatura": temperatura,
        "umidade": umidade,
        "dispositivo": "simulador-pc-failsafe",
        "timestamp": datetime.now().isoformat()
    }

def main():
    client = mqtt.Client()
    logger.info("=== INICIANDO SIMULADOR DE SALVA-GUARDA ===")
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        logger.error(f"Falha ao conectar no Broker: {e}")
        sys.exit(1)

    logger.info("Conectado! Enviando dados periodicos (Ctrl+C para encerrar).")

    try:
        while True:
            dados = gerar_dados_simulados()
            payload = json.dumps(dados)
            client.publish(MQTT_TOPIC, payload)
            
            if dados["temperatura"] > 30.0:
                logger.warning(f"ENVIADO (ALERTA): {payload}")
            else:
                logger.info(f"Enviado: {payload}")
            
            time.sleep(INTERVALO_ENVIO)
            
    except KeyboardInterrupt:
        logger.info("\nEncerrando o simulador...")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
