from logger import registrar


def mostrar_debug(texto, convocados, nomes):
    registrar("\n" + "=" * 60)
    registrar("DEBUG")
    registrar("=" * 60)

    registrar(f"Tamanho do texto: {len(texto)} caracteres")

    cargos = [
        "MÉDICO VETERINÁRIO",
        "VETERINÁRIO",
        "MÉDICO VETERINARIO",
        "VETERINARIO"
    ]

    registrar("\nOcorrências dos cargos:")

    encontrou = False

    texto_maiusculo = texto.upper()

    for cargo in cargos:
        qtd = texto_maiusculo.count(cargo)

        if qtd:
            encontrou = True
            registrar(f"  {cargo}: {qtd}")

            indice = texto_maiusculo.find(cargo)

            inicio = max(0, indice - 250)
            fim = min(len(texto), indice + 600)

            registrar("\nTrecho encontrado:\n")
            registrar(texto[inicio:fim])
            registrar("\n" + "-" * 60)

    if not encontrou:
        registrar("Nenhuma ocorrência de Médico Veterinário.")

    registrar(f"\nConvocados extraídos: {len(convocados)}")
    registrar(f"Nomes monitorados: {len(nomes)}")
    registrar("=" * 60)