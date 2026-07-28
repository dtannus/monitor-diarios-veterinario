from bs4 import BeautifulSoup

from rede import baixar_pagina
from executor import executar
from controle import ultima_edicao

URL = "https://www.ipero.sp.gov.br/nossa-cidade/concurso-publico/concurso-publico-2025"

# PDFs que não interessam para monitoramento
IGNORAR = [
    "GABARITO",
    "RESULTADO",
    "CLASSIFICA",
    "HOMOLOGA",
    "PROVA",
    "LOCAL",
    "CADERNO",
    "RECURSO",
    "RESPOSTA",
    "INSCRI",
    "DEFERIMENTO",
    "INDEFERIMENTO",
]

# PDFs que normalmente indicam movimentação importante
INTERESSE = [
    "CONVOCA",
    "NOMEA",
    "CHAMA",
    "POSSE",
]


def buscar():

    print("Acessando Concurso Público de Iperó...")

    html = baixar_pagina(URL)

    if not html:
        print("❌ Não foi possível acessar a página.")
        return

    soup = BeautifulSoup(html, "html.parser")

    ultima = ultima_edicao("Iperó")
    print(repr(ultima))

    print("Última edição analisada:", ultima)

    novas = []

    for link in soup.find_all("a", href=True):

        href = link["href"]

        if href.startswith("/"):
            href = "https://www.ipero.sp.gov.br" + href

        if not href.lower().endswith(".pdf"):
            continue

        titulo = (
            link.get_text(" ", strip=True)
            + " "
            + link.get("title", "")
        ).upper()

        # Ignora documentos sem interesse
        if any(p in titulo for p in IGNORAR):
            continue

        # Se tiver título e não indicar convocação, ignora
        if titulo.strip() and not any(p in titulo for p in INTERESSE):
            continue

        numero = href

        if ultima is not None and numero == ultima:
            continue

        novas.append({
            "numero": numero,
            "titulo": titulo,
            "url": href
        })

    if not novas:
        print("✅ Nenhum PDF novo.")
        return

    print(f"Foram encontrados {len(novas)} PDF(s) novo(s).")

    for pdf in novas:

        executar(
            cidade="Iperó",
            numero=pdf["numero"],
            data="",
            url_pdf=pdf["url"]
        )