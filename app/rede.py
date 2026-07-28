import re
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def baixar_pagina(url):
    try:
        print(f"Acessando: {url}")

        resposta = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
            allow_redirects=True
        )

        print("Status:", resposta.status_code)
        print("URL final:", resposta.url)

        resposta.raise_for_status()

        return resposta.text

    except requests.exceptions.RequestException as e:
        print(type(e).__name__)
        print(e)
        return None


def baixar_pdf(url):
    try:
        print(f"Baixando PDF: {url}")

        resposta = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
            allow_redirects=True
        )

        resposta.raise_for_status()

        return resposta.content

    except requests.exceptions.RequestException as e:
        print(type(e).__name__)
        print(e)
        return None

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