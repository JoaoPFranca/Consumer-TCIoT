"""
Configuracoes centrais do projeto MQTT.
"""
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_TOPIC = "trabalho-tc-iot/caiodaniel-joaopedro/temperatura"
MQTT_QOS = 1
MQTT_KEEPALIVE = 60

# Persistencia e Alertas
ARQUIVO_DADOS = "dados.json"
LIMITE_TEMPERATURA = 30.0
LIMITE_UMIDADE_MAX = 60.0
LIMITE_UMIDADE_MIN = 30.0
INTERVALO_ENVIO = 5
