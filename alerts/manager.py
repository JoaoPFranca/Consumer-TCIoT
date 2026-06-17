"""
Centraliza o processamento e roteamento de alertas.
"""
from .channels.console import ConsoleAlert
from .channels.discord import DiscordAlert
from config import LIMITE_TEMPERATURA

class AlertManager:
    def __init__(self):
        self.channels = [ConsoleAlert(), DiscordAlert()]

    def processar_leitura(self, dados):
        """Avalia limites e dispara notificacoes."""
        temp = dados.get("temperatura")
        disp = dados.get("dispositivo", "Desconhecido")
        
        if temp is None: return

        if temp > LIMITE_TEMPERATURA + 5:
            self.notificar(f"CRITICO: {temp}C no {disp}!", "CRITICO")
        elif temp > LIMITE_TEMPERATURA:
            self.notificar(f"AVISO: {temp}C no {disp}.", "AVISO")

    def notificar(self, msg, nivel):
        for canal in self.channels:
            try:
                canal.enviar(msg, nivel)
            except Exception as e:
                print(f"Erro no canal {canal.__class__.__name__}: {e}")
