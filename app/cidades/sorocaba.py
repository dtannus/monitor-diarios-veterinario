from logger import registrar
from rede import baixar_pagina
from executor import executar
from controle import ultima_edicao
from modelos import ResultadoCidade
from resumo import adicionar
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
        r'<a\s+href="(?P<url>https://[^"]+\.pdf)"[^>]*class="link-jornal".*?'
        r'Edição\s*n[ºo]\s*(?P<numero>\d+)\s*(?:&#8211;|–|-)\s*'
        r'(?P<dia>\d{2})\s+DE\s+(?P<mes>[A-ZÇ]+)\s+DE\s+(?P<ano>\d{4})',
        re.IGNORECASE | re.DOTALL
    )

    edicoes = []

    for match in regex.finditer(html):

        numero = int(match.group("numero"))
        dia = match.group("dia")
        mes = match.group("mes").upper()
        ano = match.group("ano")

        data = f"{dia}/{mes}/{ano}"
        url_pdf = match.group("url")

        edicoes.append((numero, data, url_pdf))

    edicoes.sort(key=lambda x: (x[0], x[2]))
    return edicoes


def buscar():

    registrar("Acessando Jornal do Município de Sorocaba...")

    html = baixar_pagina(URL)

    if not html:
        registrar("❌ Não foi possível acessar o portal.")

        resultado = ResultadoCidade(cidade="Sorocaba")
        resultado.erros.append("Não foi possível verificar o Diário Oficial.")

        adicionar(
            "❌ <b>Sorocaba</b>: não foi possível verificar o Diário Oficial."
        )

        return resultado

    ultima = ultima_edicao("Sorocaba")

    registrar(f"Última edição analisada: {ultima}")

    edicoes = extrair_edicoes(html)

    registrar(f"Edições encontradas: {[e[0] for e in edicoes]}")

    if not edicoes:
        registrar("❌ Nenhuma edição encontrada.")
        return

    novas = [
        edicao
        for edicao in edicoes
        if ultima is None or edicao[0] > ultima
    ]

    registrar(f"Novas edições: {[e[0] for e in novas]}")

    if not novas:
        registrar("✅ Nenhuma edição nova.")
        return

    registrar(f"Foram encontradas {len(novas)} edição(ões) nova(s).")

    for numero, data, url_pdf in novas:
        analisar_edicao(numero, data, url_pdf)


def testar_edicao(numero):

    html = baixar_pagina(URL)

    if not html:
        registrar("❌ Não foi possível acessar o portal.")
        return

    edicoes = extrair_edicoes(html)

    registrar(f"Edições encontradas: {[e[0] for e in edicoes]}")

    encontrou = False

    for edicao_numero, data, url_pdf in edicoes:

        if edicao_numero == int(numero):
            encontrou = True
            analisar_edicao(edicao_numero, data, url_pdf)

    if not encontrou:
        registrar("❌ Edição não encontrada.")