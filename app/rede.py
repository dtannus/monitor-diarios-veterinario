import re
import time
import requests

from logger import registrar

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def _requisicao(url, timeout=30):
    for tentativa in range(1, 4):
        try:
            registrar(f"Acessando: {url}")

            resposta = requests.get(
                url,
                headers=HEADERS,
                timeout=timeout,
                allow_redirects=True
            )

            registrar("Status:", resposta.status_code)
            registrar("URL final:", resposta.url)

            resposta.raise_for_status()

            return resposta

        except requests.exceptions.RequestException as e:
            registrar(f"Tentativa {tentativa}/3 falhou.")
            registrar(type(e).__name__)
            registrar(e)

            if tentativa < 3:
                registrar("Nova tentativa em 5 segundos...")
                time.sleep(5)
            else:
                registrar("Falha definitiva.")
                return None


def baixar_pagina(url):
    resposta = _requisicao(url, timeout=20)

    if resposta is None:
        return None

    return resposta.text


def baixar_pdf(url):
    resposta = _requisicao(url, timeout=30)

    if resposta is None:
        return None

    return resposta.content


def resolver_url_pdf(url):
    html = baixar_pagina(url)

    if not html:
        return None

    match = re.search(
        r'url=([^"\']+\.pdf)',
        html,
        re.IGNORECASE
    )

    if not match:
        registrar("PDF não encontrado na página de redirecionamento.")
        return None

    pdf = match.group(1)

    if pdf.startswith("/"):
        pdf = "https://www.vinhedo.sp.gov.br" + pdf

    return pdf