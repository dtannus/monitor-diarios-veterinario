import re


def normalizar(texto):
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)
    return texto


def procurar_nomes(texto, nomes):

    resultados = []

    texto_normalizado = normalizar(texto)

    for nome in nomes:

        nome_normalizado = normalizar(nome)

        inicio = 0

        while True:

            pos = texto_normalizado.find(nome_normalizado, inicio)

            if pos == -1:
                break

            trecho_inicio = max(0, pos - 250)
            trecho_fim = min(len(texto), pos + len(nome) + 250)

            trecho = texto[trecho_inicio:trecho_fim]

            resultados.append({
                "nome": nome,
                "trecho": trecho
            })

            inicio = pos + len(nome)

    return resultados