from extrator_pdf import extrair_texto
from analisador import analisar_texto


arquivo = "dados/pdfs/teste.pdf"

texto = extrair_texto(arquivo)

if texto:
    resultado = analisar_texto(texto)

    for item in resultado:
        print("\nTERMOS:")
        print(item["termo"])

        print("\nTRECHO:")
        print(item["trecho"])
        print("-" * 50)