import paho.mqtt.client as mqtt

MQTT_CLIENT_ID = "caiodaniel-joaopedro-subscriber"
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "trabalho-tc-iot/caiodaniel-joaopedro"

def setup(client, userdata, flags, conexao):
    if conexao == 0:
        print("Conexão com o broker realizada com sucesso")
        client.subscribe(MQTT_TOPIC)
        print(f"Assinatura do tópico {MQTT_TOPIC} realizada com sucesso")
    else:
        print("Não foi possível realizar a conexão com o broker")

def mensagem(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def main():
    client = mqtt.Client()
    client.on_connect = setup
    client.on_message = mensagem

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()