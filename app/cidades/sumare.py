import requests
from bs4 import BeautifulSoup

from executor import executar
from controle import ultima_edicao

URL = "https://dom.sumare.sp.gov.br/?edicao=todas"


def analisar_edicao(numero, data, url_pdf):
    executar("Sumaré", numero, data, url_pdf)


def extrair_edicoes(html):

    soup = BeautifulSoup(html, "html.parser")

    edicoes = []

    for card in soup.find_all("div", class_="card"):

        titulo = card.find("div", class_="file-title")
        link = card.find("a", href=True)

        if not titulo or not link:
            continue

        try:
            numero = int(
                titulo.get_text(strip=True)
                .replace("Edição", "")
                .strip()
            )
        except ValueError:
            continue

        data = None

        for texto in card.stripped_strings:
            if "/" in texto:
                data = texto.strip()
                break

        edicoes.append(
            (
                numero,
                data,
                link["href"]
            )
        )

    edicoes.sort(key=lambda x: x[0])

    return edicoes


def buscar():

    print("Acessando Diário Oficial de Sumaré...")

    resposta = requests.get(URL, timeout=30)
    resposta.raise_for_status()

    html = resposta.text

    ultima = ultima_edicao("Sumaré")

    print(f"Última edição analisada: {ultima}")

    edicoes = extrair_edicoes(html)

    if not edicoes:
        print("❌ Nenhuma edição encontrada.")
        return

    novas = [
        e for e in edicoes
        if ultima is None or e[0] > ultima
    ]

    if not novas:
        print("✅ Nenhuma edição nova.")
        return

    print(f"Foram encontradas {len(novas)} edição(ões) nova(s).")

    for numero, data, url_pdf in novas:
        analisar_edicao(
            numero,
            data,
            url_pdf
        )


def testar_edicao(numero):

    resposta = requests.get(URL, timeout=30)
    resposta.raise_for_status()

    edicoes = extrair_edicoes(resposta.text)

    for edicao_numero, data, url_pdf in edicoes:

        if edicao_numero == int(numero):

            analisar_edicao(
                edicao_numero,
                data,
                url_pdf
            )
            return

    print("❌ Edição não encontrada.")