from datetime import datetime
import os

ARQUIVO_LOG = "logs/monitor.log"


def registrar(mensagem):
    os.makedirs("logs", exist_ok=True)

    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    linha = f"[{agora}] {mensagem}"

    print(linha)

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")