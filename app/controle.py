import json
import os

BASE = os.path.dirname(os.path.dirname(__file__))

ARQUIVO = os.path.join(BASE, "dados", "controle.json")


def ler_controle():

    if not os.path.exists(ARQUIVO):
        return {}

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def ultima_edicao(cidade):

    dados = ler_controle()

    return dados.get(cidade)


def atualizar_edicao(cidade, edicao):

    dados = ler_controle()

    dados[cidade] = edicao

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )