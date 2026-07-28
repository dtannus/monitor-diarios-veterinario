def mostrar_debug(texto, convocados, nomes):
    print("\n" + "=" * 60)
    print("DEBUG")
    print("=" * 60)

    print(f"Tamanho do texto: {len(texto)} caracteres")

    cargos = [
        "MÉDICO VETERINÁRIO",
        "VETERINÁRIO",
        "MÉDICO VETERINARIO",
        "VETERINARIO"
    ]

    print("\nOcorrências dos cargos:")

    encontrou = False

    texto_maiusculo = texto.upper()

    for cargo in cargos:
        qtd = texto_maiusculo.count(cargo)

        if qtd:
            encontrou = True
            print(f"  {cargo}: {qtd}")

            indice = texto_maiusculo.find(cargo)

            inicio = max(0, indice - 250)
            fim = min(len(texto), indice + 600)

            print("\nTrecho encontrado:\n")
            print(texto[inicio:fim])
            print("\n" + "-" * 60)

    if not encontrou:
        print("Nenhuma ocorrência de Médico Veterinário.")

    print(f"\nConvocados extraídos: {len(convocados)}")
    print(f"Nomes monitorados: {len(nomes)}")
    print("=" * 60)