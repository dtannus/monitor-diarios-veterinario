from rede import baixar_pagina
from executor import executar
from controle import ultima_edicao
import re

URL = "https://noticias.sorocaba.sp.gov.br/jornal/"


def analisar_edicao(numero, data, url_pdf):
    executar("Sorocaba", numero, data, url_pdf)


def extrair_edicoes(html):
    """
    Extrai todas as edições encontradas na página.

    Retorna:
        [(numero, data, url_pdf), ...]
    """

    regex = re.compile(
        r'https://[^"]+/(\d+)-(\d{2})-DE-([A-ZÇ]+)-DE-(\d{4})(?:-\d+)?\.pdf',
        re.IGNORECASE
    )

    edicoes = []

    for match in regex.finditer(html):

        numero = int(match.group(1))
        dia = match.group(2)
        mes = match.group(3)
        ano = match.group(4)

        data = f"{dia}/{mes}/{ano}"
        url_pdf = match.group(0)

        edicoes.append((numero, data, url_pdf))

    edicoes.sort(key=lambda x: x[0])

    return edicoes


def buscar():

    print("Acessando Jornal do Município de Sorocaba...")

    html = baixar_pagina(URL)

    if not html:
        print("❌ Não foi possível acessar o portal.")
        return

    ultima = ultima_edicao("Sorocaba")

    print(f"Última edição analisada: {ultima}")

    edicoes = extrair_edicoes(html)

    if not edicoes:
        print("❌ Nenhuma edição encontrada.")
        return

    novas = [
        edicao
        for edicao in edicoes
        if ultima is None or edicao[0] > ultima
    ]

    if not novas:
        print("✅ Nenhuma edição nova.")
        return

    print(f"Foram encontradas {len(novas)} edição(ões) nova(s).")

    for numero, data, url_pdf in novas:
        analisar_edicao(numero, data, url_pdf)


def testar_edicao(numero):

    html = baixar_pagina(URL)

    if not html:
        print("❌ Não foi possível acessar o portal.")
        return

    edicoes = extrair_edicoes(html)

    for edicao_numero, data, url_pdf in edicoes:

        if edicao_numero == int(numero):
            analisar_edicao(edicao_numero, data, url_pdf)
            return

    print("❌ Edição não encontrada.")