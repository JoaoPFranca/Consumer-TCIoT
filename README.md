# Consumer-TCIoT: Sistema de Monitoramento MQTT

Este projeto implementa um sistema simples de Internet das Coisas (IoT) para monitoramento de temperatura e umidade usando o protocolo MQTT.

## Funcionalidades

- Configuracao Centralizada: Facil de alterar broker e topicos em um unico arquivo.
- Subscriber Robusto: Recebe dados, exibe logs detalhados e salva tudo em um arquivo dados.json.
- Sistema de Alertas Desacoplado: Gerenciamento profissional de notificacoes via Console e Discord.
- Variaveis de Ambiente: Uso de arquivo .env para seguranca de credenciais e webhooks.
- Publisher Simulador: Script Python para simular um sensor DHT22 no computador.
- Compatibilidade ESP32: Codigo pronto para rodar em MicroPython (Wokwi ou hardware real).

## Requisitos

- Python 3.x instalado.
- Dependencias listadas em `requirements.txt`.

## Instalacao

1. Clone o repositorio ou baixe os arquivos.
2. Instale as dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure as variaveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`.
   - Preencha o `DISCORD_ALERT_WEBHOOK` no arquivo `.env`.

## Como Usar

### 1. Iniciando o Assinante (Subscriber)
O ponto de entrada principal e o arquivo `main.py`:
```bash
python main.py
```

### 2. Enviando Dados
Voce tem duas opcoes para enviar dados:

#### Opcao A: Simulador no PC
```bash
python publisher.py
```

#### Opcao B: ESP32 (MicroPython / Wokwi)
Carregue o arquivo `publisher_esp32.py` no seu ESP32. O codigo esta configurado para o sensor DHT22 no Pino 15.

## Estrutura do Projeto

- `main.py`: Ponto de entrada que inicializa o sistema.
- `subscriber.py`: Classe principal de processamento de dados.
- `alerts/`: Modulo de gerenciamento de alertas (Console e Discord).
- `config.py`: Configuracoes do broker, porta e topicos.
- `.env`: Variaveis de ambiente sensiveis (nao versionado).
- `publisher.py`: Simulador de sensor para rodar no computador.
- `publisher_esp32.py`: Versao do publicador para MicroPython.
- `dados.json`: Historico de leituras.

## Desenvolvedores
- Caio Daniel Fonseca de Araujo
- Joao Pedro de Franca Barboza

## Disciplina
IMD0907 - Tecnologias de Comunicação para Internet das Coisas (2026.1) - Turma 01
