from extrator_pdf import extrair_texto


arquivo = "dados/pdfs/teste.pdf"


texto = extrair_texto(arquivo)


if texto:
    print("PDF lido com sucesso!")
    print()
    print(texto[:1000])
else:
    print("Não foi possível extrair texto.")