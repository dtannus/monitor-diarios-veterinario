from datetime import datetime
from zoneinfo import ZoneInfo
import os

os.makedirs("logs", exist_ok=True)

ARQUIVO_LOG = os.path.join(
    "logs",
    datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d") + ".log"
)


def registrar(*mensagens):

    texto = " ".join(str(m) for m in mensagens)

    agora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")
    linha = f"[{agora}] {texto}"

    print(texto)

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")