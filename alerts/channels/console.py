"""
Modulo de Alerta via Console.
"""

class ConsoleAlert:
    # Codigos ANSI para cores
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    def enviar(self, mensagem, nivel="AVISO"):
        """Exibe o alerta colorido no terminal."""
        cor = self.YELLOW if nivel == "AVISO" else self.RED
        print(f"{cor}{self.BOLD}[{nivel}] {mensagem}{self.RESET}")
