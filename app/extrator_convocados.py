import re

PADRAO_CARGO = re.compile(
    r"MÉDICO\s+VETERINÁRIO"
    r"|MÉDICO\s+VETERINARIO"
    r"|VETERINÁRIO"
    r"|VETERINARIO",
    re.IGNORECASE,
)

PADROES = [

    (
        "Prorrogação de posse",
        re.compile(
            r"prorroga(?:r|ção)?.{0,150}?posse\s+de\s+([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]{5,120})",
            re.IGNORECASE | re.DOTALL,
        ),
    ),

    (
        "Posse",
        re.compile(
            r"posse\s+de\s+([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]{5,120})",
            re.IGNORECASE,
        ),
    ),

    (
        "Nomeação",
        re.compile(
            r"nomead[oa].{0,40}?\s+([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]{5,120})",
            re.IGNORECASE | re.DOTALL,
        ),
    ),

    (
        "Convocação",
        re.compile(
            r"convocad[oa]?\s+([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]{5,120})",
            re.IGNORECASE,
        ),
    ),

    (
        "Convocação",
        re.compile(
            r"convoca.{0,40}?\s+([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ\s]{5,120})",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
]


def limpar_nome(nome):

    nome = " ".join(nome.split())

    if len(nome.split()) < 2:
        return None

    proibidas = [
        "PORTARIA",
        "DECRETO",
        "LEI",
        "SECRETÁRIO",
        "SECRETARIA",
        "PREFEITURA",
        "PALÁCIO",
        "MUNICÍPIO",
        "CARGO",
        "MÉDICO",
        "VETERINÁRIO",
        "VETERINARIO",
        "CONCURSO",
        "PROCESSO",
        "EDITAL",
        "ARTIGO",
        "RECURSOS HUMANOS",
    ]

    texto = nome.upper()

    for palavra in proibidas:
        if palavra in texto:
            return None

    return nome


def extrair_convocados(texto):

    resultados = []
    vistos = set()

    for ocorrencia in PADRAO_CARGO.finditer(texto):

        cargo = ocorrencia.group(0).upper()
        pos = ocorrencia.start()

        contexto_inicio = max(0, pos - 1500)
        contexto_fim = min(len(texto), pos + 300)

        contexto = texto[contexto_inicio:contexto_fim]

        for tipo, regex in PADROES:

            encontrados = list(regex.finditer(contexto))

            if not encontrados:
                continue

            candidato = encontrados[-1].group(1)

            nome = limpar_nome(candidato)

            if nome is None:
                continue

            chave = (nome, cargo)

            if chave in vistos:
                continue

            vistos.add(chave)

            resultados.append(
                {
                    "nome": nome,
                    "cargo": cargo,
                    "tipo": tipo,
                    "trecho": contexto,
                }
            )

            break

    return resultados