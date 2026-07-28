import json
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(__file__))

ARQUIVO = os.path.join(BASE, "dados", "historico.json")


def salvar_resultado(
    cidade,
    convocacoes,
    nomes=None,
    edicao=None,
    data_publicacao=None
):

    registro = {
        "data_busca": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "cidade": cidade,
        "edicao": edicao,
        "data_publicacao": data_publicacao,
        "convocacoes": convocacoes,
        "nomes_encontrados": nomes if nomes else []
    }

    historico = []

    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
                historico = json.load(arquivo)
        except Exception:
            historico = []

    historico.append(registro)

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(
            historico,
            arquivo,
            indent=4,
            ensure_ascii=False
        )