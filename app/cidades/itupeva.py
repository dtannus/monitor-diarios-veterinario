import json
import re

from rede import baixar_pagina
from executor import executar
from controle import ultima_edicao


URL_API = (
    "https://dosp.com.br/api/index.php/"
    "dioecadernos.js/4924/5511?callback=dioe"
)


def interpretar_resposta(resposta):

    if not resposta:
        print("❌ Resposta vazia da API.")
        return None

    # Remove o wrapper JSONP:
    # dioe({...});
    resposta = resposta.strip()

    match = re.search(
        r"dioe\s*\(\s*(\{.*\})\s*\)\s*;?\s*$",
        resposta,
        re.DOTALL
    )

    if not match:
        print("❌ API JSONP está incompleta.")
        return None

    try:
        return json.loads(match.group(1))

    except json.JSONDecodeError as erro:
        print("❌ Erro ao interpretar JSON da API:")
        print(erro)
        return None


def analisar_publicacao(publicacao):

    iddo = publicacao["iddo"]
    numero = publicacao["edicao_do"]
    data = publicacao["data"]

    # O site usa Base64 do iddo para acessar o PDF.
    import base64

    codigo = base64.b64encode(
        str(iddo).encode()
    ).decode()

    url_pdf = f"https://dosp.com.br/exibe_do.php?i={codigo}"

    executar(
        cidade="Itupeva",
        numero=numero,
        data=data,
        url_pdf=url_pdf
    )

    return iddo


def buscar():

    print("Acessando Diário Oficial de Itupeva...")

    resposta = baixar_pagina(URL_API)

    dados = interpretar_resposta(resposta)

    if not dados:
        print("❌ Não foi possível interpretar a API.")

        return

    if "data" not in dados:
        print("❌ API retornou um formato inesperado.")

        return

    ultima = ultima_edicao("Itupeva")

    print("Último ID processado:", ultima)

    try:
        ultima_id = int(ultima) if ultima is not None else None

    except (TypeError, ValueError):
        print("⚠️ Controle de Itupeva inválido.")
        ultima_id = None

    novas = []

    for publicacao in dados["data"]:

        # Ignora Câmara Municipal
        if publicacao.get("cadernos_texto") != "Caderno Executivo":
            continue

        iddo = publicacao.get("iddo")

        if iddo is None:
            continue

        try:
            iddo = int(iddo)

        except (TypeError, ValueError):
            continue

        if ultima_id is None or iddo > ultima_id:
            novas.append(publicacao)

    if not novas:

        print("✅ Nenhuma publicação nova.")

        return

    # A API normalmente vem do mais recente para o mais antigo.
    # Processamos na ordem cronológica.
    novas.sort(key=lambda x: int(x["iddo"]))

    print(
        f"Foram encontradas {len(novas)} "
        f"publicação(ões) nova(s) do Caderno Executivo."
    )

    maior_id = ultima_id

    for publicacao in novas:

        iddo = analisar_publicacao(publicacao)

        if maior_id is None or iddo > maior_id:
            maior_id = iddo

    # Atualiza o controle somente depois do processamento.
    from controle import atualizar_edicao

    atualizar_edicao("Itupeva", maior_id)

    print(
        f"Controle atualizado: Itupeva -> {maior_id}"
    )


def testar_edicao(numero):

    print(f"Procurando edição {numero}...")

    resposta = baixar_pagina(URL_API)

    dados = interpretar_resposta(resposta)

    if not dados:
        print("❌ Não foi possível interpretar a API.")

        return

    if "data" not in dados:
        print("❌ API retornou um formato inesperado.")

        return

    encontrados = []

    for publicacao in dados["data"]:

        if str(publicacao.get("edicao_do")) != str(numero):
            continue

        # Para o teste do monitor, somente Executivo.
        if publicacao.get("cadernos_texto") != "Caderno Executivo":
            continue

        encontrados.append(publicacao)

    if not encontrados:

        print(
            f"❌ Edição {numero} não possui "
            "publicação do Caderno Executivo na API."
        )

        return

    # Se houver mais de um PDF Executivo na mesma edição,
    # todos serão testados.
    for publicacao in encontrados:

        analisar_publicacao(publicacao)