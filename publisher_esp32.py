"""
Publicador (Publisher) - MicroPython para ESP32.
Este script le dados de um sensor DHT22 e os envia via MQTT.
Projetado para rodar no Wokwi ou hardware real.
"""
import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# Parametros Wi-Fi (Padrao Wokwi)
WIFI_SSID       = 'Wokwi-GUEST'
WIFI_PASSWORD   = ''

# Parametros MQTT
MQTT_CLIENT_ID  = "esp32-sensor-caiodaniel"
MQTT_BROKER     = "broker.mqttdashboard.com"
MQTT_TOPIC      = "trabalho-tc-iot/caiodaniel-joaopedro/temperatura"

# Sensor no Pino 15
sensor = dht.DHT22(Pin(15))

def conectar_wifi():
    """Conecta ao Wi-Fi usando o padrao mais compativel com Wokwi."""
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Conectando ao Wi-Fi (SSID: {}) ".format(WIFI_SSID), end="")
    
    if sta_if.isconnected():
        print("Ja estava conectado!")
        return
    
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    
    print(" Conectado!")
    print("IP:", sta_if.ifconfig()[0])

def conectar_mqtt():
    """Conecta ao broker MQTT."""
    print("Conectando ao MQTT... ", end="")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.connect()
    print("Conectado!")
    return client

def main():
    while True:
        try:
            conectar_wifi()
            client = conectar_mqtt()
            print("Iniciando monitoramento...")
            ultima_leitura = ""
            
            while True:
                print("Lendo sensor... ", end="")
                sensor.measure()
                
                dados = {
                    "temperatura": sensor.temperature(),
                    "umidade": sensor.humidity(),
                    "dispositivo": "esp32-wokwi"
                }
                
                mensagem = ujson.dumps(dados)
                
                if mensagem != ultima_leitura:
                    print("Publicando: {}".format(mensagem))
                    client.publish(MQTT_TOPIC, mensagem)
                    ultima_leitura = mensagem
                else:
                    print("Sem alteracoes.")
                
                time.sleep(5)
                
        except Exception as e:
            print("\nOcorreu um erro: {}. Reiniciando em 5s...".format(e))
            time.sleep(5)

if __name__ == "__main__":
    main()
