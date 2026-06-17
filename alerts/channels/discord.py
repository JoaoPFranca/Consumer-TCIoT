"""
Alerta via Discord Embeds formatados.
"""
import requests
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DiscordAlert:
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_ALERT_WEBHOOK")
        self.validar()

    def validar(self):
        """Valida a conectividade com o Webhook."""
        if not self.webhook_url:
            logger.error("Webhook Discord ausente no .env")
            return
        try:
            if requests.get(self.webhook_url).status_code == 200:
                logger.info("Webhook Discord validado com sucesso.")
        except:
            logger.error("Falha ao validar conexao com Discord.")

    def enviar(self, mensagem, nivel="AVISO"):
        """Envia card formatado para o Discord."""
        if not self.webhook_url: return
        
        color = 16776960 if nivel == "AVISO" else 15548997
        titulo = "ALERTA DE MONITORAMENTO" if nivel == "AVISO" else "ALERTA CRITICO DETECTADO"
        
        payload = {
            "embeds": [
                {
                    "title": titulo,
                    "description": mensagem,
                    "color": color,
                    "fields": [
                        {
                            "name": "Nivel de Prioridade",
                            "value": nivel,
                            "inline": True
                        },
                        {
                            "name": "Status do Sistema",
                            "value": "Acao Necessaria" if nivel == "CRITICO" else "Monitorando",
                            "inline": True
                        },
                        {
                            "name": "Local/Dispositivo",
                            "value": "Sensor IoT - Area Interna",
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": "Sistema de Monitoramento IoT - Disciplina Consumer-TCIoT"
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
            ]
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Erro ao enviar para Discord: {e}")
