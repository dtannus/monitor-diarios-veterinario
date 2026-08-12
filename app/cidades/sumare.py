from bs4 import BeautifulSoup

from executor import executar
from controle import ultima_edicao
from rede import baixar_pagina
from resumo import adicionar
from edicoes import chave_ordenacao


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

        numero = (
            titulo.get_text(strip=True)
            .replace("Edição", "")
            .strip()
            .upper()
        )

        if not numero:
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

    edicoes.sort(
        key=lambda x: chave_ordenacao(x[0])
    )

    return edicoes


def buscar():

    print("Acessando Diário Oficial de Sumaré...")

    html = baixar_pagina(URL)

    if not html:
        print("❌ Não foi possível acessar o Diário Oficial de Sumaré.")

        adicionar(
            "❌ <b>Sumaré</b>: não foi possível verificar o Diário Oficial."
        )

        return

    ultima = ultima_edicao("Sumaré")

    print(f"Última edição analisada: {ultima}")

    edicoes = extrair_edicoes(html)

    if not edicoes:
        print("❌ Nenhuma edição encontrada.")

        adicionar(
            "❌ <b>Sumaré</b>: nenhuma edição foi encontrada."
        )

        return

    novas = []

    ultima_base = (
        str(ultima).split("-")[0]
        if ultima is not None
        else None
    )

    for numero, data, url_pdf in edicoes:

        base = str(numero).split("-")[0]

        if ultima_base is None or int(base) > int(ultima_base):
            novas.append((numero, data, url_pdf))

    if not novas:
        print("✅ Nenhuma edição nova.")
        return

    print(f"Foram encontradas {len(novas)} edição(ões) nova(s).")

    ultima_processada = None

    for numero, data, url_pdf in novas:

        analisar_edicao(
            numero,
            data,
            url_pdf
        )

        ultima_processada = str(numero).split("-")[0]

    if ultima_processada is not None:
        from controle import atualizar_edicao

        atualizar_edicao(
            "Sumaré",
            int(ultima_processada)
        )


def testar_edicao(numero):

    html = baixar_pagina(URL)

    if not html:
        print("❌ Não foi possível acessar o Diário Oficial de Sumaré.")
        return

    edicoes = extrair_edicoes(html)

    base_procurada = str(numero).split("-")[0]

    encontrou = False

    for edicao_numero, data, url_pdf in edicoes:

        base = str(edicao_numero).split("-")[0]

        if base == base_procurada:

            encontrou = True

            analisar_edicao(
                edicao_numero,
                data,
                url_pdf
            )

        elif encontrou:
            break

    if not encontrou:
        print("❌ Edição não encontrada.")