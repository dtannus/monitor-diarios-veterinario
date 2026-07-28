import re
from configuracao import PALAVRAS_CHAVE, TERMOS_CONVOCACAO


def normalizar(texto):
    return re.sub(r"\s+", " ", texto.lower())


def procurar_convocacoes(texto):

    texto_limpo = normalizar(texto)

    resultados = []

    for cargo in PALAVRAS_CHAVE:

        posicao = texto_limpo.find(cargo.lower())

        while posicao != -1:

            inicio = max(0, posicao - 500)
            fim = min(len(texto_limpo), posicao + 500)

            trecho = texto[inicio:fim]

            trecho_limpo = normalizar(trecho)

            encontrados = []

            for termo in TERMOS_CONVOCACAO:
                if termo.lower() in trecho_limpo:
                    encontrados.append(termo)

            if encontrados:

                resultados.append({
                    "cargo": cargo,
                    "termos": encontrados,
                    "trecho": trecho
                })

            posicao = texto_limpo.find(
                cargo.lower(),
                posicao + len(cargo)
            )

    return resultados