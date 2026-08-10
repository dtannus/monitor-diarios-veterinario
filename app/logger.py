from datetime import datetime
import os

os.makedirs("logs", exist_ok=True)

ARQUIVO_LOG = os.path.join(
    "logs",
    datetime.now().strftime("%Y-%m-%d") + ".log"
)


def registrar(*mensagens):

    texto = " ".join(str(m) for m in mensagens)

    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"[{agora}] {texto}"

    print(texto)

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")