"""
Projeto: Sistema de Monitoramento de Temperatura via MQTT
Disciplina: IMD0907 - Tecnologias de Comunicação para Internet das Coisas (2026.1)
Turma: 01

Desenvolvedores:
    - Caio Daniel Fonseca de Araújo
    - João Pedro França Barboza

Descrição:
    Conexão Wi-Fi e MQTT com broker público. Loop mínimo publicando
    uma mensagem de teste para validar a comunicação.
"""

import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# Configurações Wi-Fi e MQTT
WIFI_SSID       = 'Wokwi-GUEST'
WIFI_PASSWORD   = ''
MQTT_CLIENT_ID  = "esp32-sensor-caiodaniel"
MQTT_BROKER     = "broker.mqttdashboard.com"
MQTT_TOPIC      = "trabalho-tc-iot/caiodaniel-joaopedro/temperatura"
MQTT_QOS        = 1
MQTT_KEEPALIVE  = 60

# Inicialização do sensor DHT22 no Pino 15 (Padrão Wokwi)
sensor = dht.DHT22(Pin(15))

def conectar_wifi():
    """Conecta o dispositivo à rede Wi-Fi de forma robusta no Wokwi."""
    print("Conectando ao Wi-Fi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    
    # Se já estiver conectado, não faz nada
    if sta_if.isconnected():
        print(" Já estava conectado!")
        return
    
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    
    # Timeout de 15 segundos para conexão
    tentativas = 0
    while not sta_if.isconnected() and tentativas < 150:
        print(".", end="")
        time.sleep(0.1)
        tentativas += 1
        
    if sta_if.isconnected():
        print(" Conectado!")
        print("Configuração IP:", sta_if.ifconfig())
    else:
        print(" Falha ao conectar! Verifique o Wokwi.")

def conectar_mqtt():
    """Conecta ao broker MQTT."""
    print("Conectando ao broker MQTT... ", end="")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, keepalive=MQTT_KEEPALIVE)
    client.connect()
    print("Conectado!")
    return client

def main():
    conectar_wifi()
    
    # Pequeno delay após o Wi-Fi estabilizar
    time.sleep(1)
    
    try:
        client = conectar_mqtt()
    except Exception as e:
        print("Erro ao conectar ao MQTT:", e)
        # Tenta reconectar mais tarde
        time.sleep(5)
        return

    print("Iniciando monitoramento...")
    ultima_leitura = ""

    while True:
        try:
            print("Medindo condições climáticas... ", end="")
            sensor.measure()
            
            # Prepara os dados no formato esperado pelo subscriber
            dados = {
                "temperatura": sensor.temperature(),
                "umidade": sensor.humidity(),
                "dispositivo": "esp32-wokwi"
            }
            
            mensagem = ujson.dumps(dados)
            
            # Envia apenas se houver mudança para economizar banda
            if mensagem != ultima_leitura:
                print("Atualizado!")
                print("Publicando no tópico {}: {}".format(MQTT_TOPIC, mensagem))
                client.publish(MQTT_TOPIC, mensagem, qos=MQTT_QOS)
                ultima_leitura = mensagem
            else:
                print("Sem alterações")
            
            time.sleep(2)
            
        except Exception as e:
            print("\nErro durante o loop:", e)
            # Verifica se o Wi-Fi caiu
            sta_if = network.WLAN(network.STA_IF)
            if not sta_if.isconnected():
                conectar_wifi()
            
            time.sleep(5)
            try:
                client.connect()
            except:
                pass

if __name__ == "__main__":
    main()

