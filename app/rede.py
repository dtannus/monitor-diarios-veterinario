import re
import time
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def _requisicao(url, timeout=30):
    for tentativa in range(1, 4):
        try:
            print(f"Acessando: {url}")

            resposta = requests.get(
                url,
                headers=HEADERS,
                timeout=timeout,
                allow_redirects=True
            )

            print("Status:", resposta.status_code)
            print("URL final:", resposta.url)

            resposta.raise_for_status()

            return resposta

        except requests.exceptions.RequestException as e:
            print(f"Tentativa {tentativa}/3 falhou.")
            print(type(e).__name__)
            print(e)

            if tentativa < 3:
                print("Nova tentativa em 5 segundos...")
                time.sleep(5)
            else:
                print("Falha definitiva.")
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
        print("PDF não encontrado na página de redirecionamento.")
        return None

    pdf = match.group(1)

    if pdf.startswith("/"):
        pdf = "https://www.vinhedo.sp.gov.br" + pdf

    return pdf