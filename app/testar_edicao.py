from rede import baixar_pagina, baixar_pdf
from extrator_pdf import extrair_texto
from analisador import analisar
from nomes import procurar_nomes
from configuracao import NOMES_MONITORADOS
import json

BASE = "https://portal-adm.campinas.sp.gov.br"

edicao = input("Número da edição: ")

url = f"https://portal-adm.campinas.sp.gov.br/api/v1/publicacoes-dom/edicao/{edicao}"

print("Consultando API...")

resposta = baixar_pagina(url)

if not resposta:
    print("Edição não encontrada.")
    exit()

dados = json.loads(resposta)

arquivo = dados["dom_arquivo"]

pdf = baixar_pdf(BASE + arquivo)

print("Extraindo texto...")

texto = extrair_texto(pdf)

print("\n========== CONVOCAÇÕES ==========\n")

resultado = analisar(texto)

if resultado:

    for r in resultado:

        print("Cargo:", r["cargo"])
        print("Termos:", ", ".join(r["termos"]))
        print()
        print(r["trecho"])
        print("\n" + "=" * 60)

else:

    print("Nenhuma convocação encontrada.")

print("\n========== NOMES ==========\n")

nomes = procurar_nomes(texto, NOMES_MONITORADOS)

if nomes:

    for n in nomes:

        print(n["nome"])
        print()
        print(n["trecho"])
        print("\n" + "=" * 60)

else:

    print("Nenhum nome encontrado.")