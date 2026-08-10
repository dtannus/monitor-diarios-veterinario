from logger import registrar
from rede import baixar_pagina, resolver_url_pdf
from executor import executar
from controle import ultima_edicao
from modelos import ResultadoCidade
from resumo import adicionar
import re

URL = "https://www.vinhedo.sp.gov.br/portal/diario-oficial"


def analisar_edicao(numero, data, url_pdf):
    executar("Vinhedo", numero, data, url_pdf)


def extrair_edicoes(html):

    BASE = "https://www.vinhedo.sp.gov.br"

    blocos = re.findall(
        r'<div class="dof_publicacao_diario sw_item_listagem".*?</a>\s*</div>',
        html,
        re.DOTALL
    )

    edicoes = []

    for bloco in blocos:

        numero = re.search(
            r'Edição nº\s*(\d+)',
            bloco,
            re.IGNORECASE
        )

        data = re.search(
            r'Postagem:</strong>\s*<span>(.*?)</span>',
            bloco,
            re.DOTALL | re.IGNORECASE
        )

        download = re.search(
            r'data-href="([^"]+)"',
            bloco,
            re.IGNORECASE
        )

        if not (numero and data and download):
            continue

        numero = int(numero.group(1))
        data = data.group(1).strip()

        url_download = download.group(1)

        if url_download.startswith("/"):
            url_download = BASE + url_download

        edicoes.append(
            (
                numero,
                data,
                url_download
            )
        )

    edicoes.sort(key=lambda x: x[0])

    return edicoes


def buscar():

    registrar("Acessando Diário Oficial de Vinhedo...")

    html = baixar_pagina(URL)

    if not html:
        registrar("❌ Não foi possível acessar o portal.")

        resultado = ResultadoCidade(cidade="Vinhedo")
        resultado.erros.append("Não foi possível verificar o Diário Oficial.")

        adicionar(
            "❌ <b>Vinhedo</b>: não foi possível verificar o Diário Oficial."
        )

        return resultado

    ultima = ultima_edicao("Vinhedo")

    registrar(f"Última edição analisada: {ultima}")

    edicoes = extrair_edicoes(html)

    registrar(f"Edições encontradas: {[e[0] for e in edicoes]}")

    if not edicoes:
        registrar("❌ Nenhuma edição encontrada.")

        resultado = ResultadoCidade(cidade="Vinhedo")
        resultado.erros.append("Nenhuma edição encontrada.")

        adicionar(
            "❌ <b>Vinhedo</b>: nenhuma edição foi encontrada."
        )

        return resultado

    novas = [
        e for e in edicoes
        if ultima is None or e[0] > ultima
    ]

    registrar(f"Novas edições: {[e[0] for e in novas]}")

    if not novas:
        registrar("✅ Nenhuma edição nova.")
        return

    registrar(f"Foram encontradas {len(novas)} edição(ões) nova(s).")

    for numero, data, url_download in novas:

        url_pdf = resolver_url_pdf(url_download)

        if not url_pdf:
            registrar(f"❌ Não foi possível localizar o PDF da edição {numero}.")
            continue

        analisar_edicao(
            numero,
            data,
            url_pdf
        )


def testar_edicao(numero):

    html = baixar_pagina(URL)

    if not html:
        registrar("❌ Não foi possível acessar o portal.")
        return

    edicoes = extrair_edicoes(html)

    registrar(f"Edições encontradas: {[e[0] for e in edicoes]}")

    for edicao_numero, data, url_download in edicoes:

        if edicao_numero == int(numero):

            url_pdf = resolver_url_pdf(url_download)

            if not url_pdf:
                registrar("❌ Não foi possível localizar o PDF.")
                return

            analisar_edicao(
                edicao_numero,
                data,
                url_pdf
            )
            return

    registrar("❌ Edição não encontrada.")