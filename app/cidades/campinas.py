from rede import baixar_pagina
from executor import executar
from controle import ultima_edicao
import json

URL_API = "https://portal-adm.campinas.sp.gov.br/api/v2/publicacoes-dom"
BASE_PDF = "https://portal-adm.campinas.sp.gov.br"


def analisar_edicao(edicao):

    numero = edicao["dom_edicao"]
    data = edicao["dom_data_pub"]

    url_pdf = BASE_PDF + edicao["dom_arquivo"]

    executar(
        cidade="Campinas",
        numero=numero,
        data=data,
        url_pdf=url_pdf
    )


def buscar():

    print("Acessando Diário Oficial de Campinas...")

    resposta = baixar_pagina(URL_API)

    if not resposta:
        print("❌ Não foi possível acessar a API.")
        return

    dados = json.loads(resposta)

    if "rows" not in dados:
        print("❌ API retornou um formato inesperado.")
        return

    ultima = ultima_edicao("Campinas")

    print("Última edição analisada:", ultima)

    novas = []

    for edicao in reversed(dados["rows"]):

        numero = edicao["dom_edicao"]

        if ultima is None or int(numero) > int(ultima):
            novas.append(edicao)

    if not novas:
        print("✅ Nenhuma edição nova.")
        return

    print(f"Foram encontradas {len(novas)} edição(ões) nova(s).")

    for edicao in novas:
        analisar_edicao(edicao)


def testar_edicao(numero):

    print(f"Procurando edição {numero}...")

    resposta = baixar_pagina(URL_API)

    if not resposta:
        print("❌ Erro ao acessar a API.")
        return

    dados = json.loads(resposta)

    if "rows" not in dados:
        print("❌ API retornou um formato inesperado.")
        return

    for edicao in dados["rows"]:

        if str(edicao["dom_edicao"]) == str(numero):
            analisar_edicao(edicao)
            return

    print("❌ Edição não encontrada.")