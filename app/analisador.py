import re

from configuracao import CARGOS_PRINCIPAIS, TERMOS_CONVOCACAO


def normalizar(texto):
    return re.sub(r"\s+", " ", texto.lower())


NEGATIVOS = [
    "atendimento veterinário",
    "atendimento veterinario",
    "hospital veterinário",
    "hospital veterinario",
    "clínica veterinária",
    "clinica veterinaria",
    "medicina veterinária",
    "medicina veterinaria",
    "serviço veterinário",
    "servico veterinario",
    "cremação pet",
    "cremacao pet",
]


POSITIVOS = [
    "cargo",
    "nomeação",
    "nomeacao",
    "nomeado",
    "nomeada",
    "convocação",
    "convocacao",
    "convocado",
    "convocada",
    "posse",
    "concurso público",
    "concurso publico",
    "processo seletivo",
]


def analisar(texto):

    texto_normalizado = normalizar(texto)

    resultados = []

    for cargo in CARGOS_PRINCIPAIS:

        cargo = cargo.lower()

        inicio = 0

        while True:

            pos = texto_normalizado.find(cargo, inicio)

            if pos == -1:
                break

            trecho_inicio = max(0, pos - 300)
            trecho_fim = min(len(texto_normalizado), pos + 300)

            trecho = texto_normalizado[trecho_inicio:trecho_fim]

            pontos = 0
            motivos = []

            if "cargo" in trecho:
                pontos += 3
                motivos.append("cargo")

            for termo in TERMOS_CONVOCACAO:

                termo = termo.lower()

                if termo in trecho:

                    pontos += 2

                    if termo not in motivos:
                        motivos.append(termo)

            for termo in POSITIVOS:

                if termo in trecho:

                    if termo not in motivos:
                        motivos.append(termo)

            for termo in NEGATIVOS:

                if termo in trecho:

                    pontos -= 4

                    motivos.append(f"- {termo}")

            if pontos >= 3:

                resultados.append({

                    "cargo": cargo,
                    "pontuacao": pontos,
                    "termos": motivos,
                    "trecho": texto[trecho_inicio:trecho_fim]

                })

            inicio = pos + len(cargo)

    return resultados