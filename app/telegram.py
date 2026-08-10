import os
import time
import requests


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN não configurado.")

if not CHAT_ID:
    raise RuntimeError("TELEGRAM_CHAT_ID não configurado.")


URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def enviar_mensagem(texto, html=True):

    dados = {
        "chat_id": CHAT_ID,
        "text": texto,
        "disable_web_page_preview": True
    }

    if html:
        dados["parse_mode"] = "HTML"

    for tentativa in range(2):

        try:

            resposta = requests.post(
                URL,
                data=dados,
                timeout=20
            )

            resposta.raise_for_status()

            print("✅ Telegram: mensagem enviada.")

            return True

        except Exception as e:

            print(
                f"⚠️ Telegram: tentativa "
                f"{tentativa + 1}/2 falhou: {e}"
            )

            if tentativa == 0:
                print("🔄 Nova tentativa em 5 segundos...")
                time.sleep(5)

    print("❌ Telegram: não foi possível enviar a mensagem.")

    return False