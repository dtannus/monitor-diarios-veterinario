from debug import mostrar_debug
from rede import baixar_pdf
from extrator_pdf import extrair_texto
from texto import normalizar_texto
from analisador import analisar
from extrator_convocados import extrair_convocados
from nomes import procurar_nomes
from configuracao import NOMES_MONITORADOS
from historico import salvar_resultado
from controle import atualizar_edicao
from resumo import adicionar, marcar_convocacao


def executar(cidade, numero, data, url_pdf):

    print("\n========================================")
    print(f"{cidade} - Edição {numero} - {data}")
    print("========================================")

    adicionar(f"📍 <b>{cidade}</b>")
    adicionar(f"📰 Edição {numero} - {data}")

    print(f"URL do PDF: {url_pdf}")
    print("Baixando PDF...")

    pdf = baixar_pdf(url_pdf)

    if not pdf:
        print("❌ Erro ao baixar PDF.")
        adicionar("❌ Erro ao baixar PDF.")
        adicionar("")
        return

    print("Extraindo texto...")

    texto = extrair_texto(pdf)

    if not texto:
        print("❌ Não foi possível extrair o texto.")
        adicionar("❌ Não foi possível extrair o texto.")
        adicionar("")
        return

    texto = normalizar_texto(texto)

    resultados = analisar(texto)

    convocados = extrair_convocados(texto)

    nomes = procurar_nomes(texto, NOMES_MONITORADOS)

    mostrar_debug(texto, convocados, nomes)

    if convocados:
      
        marcar_convocacao()

        print(f"\n🐾 {len(convocados)} convocado(s) encontrado(s).\n")
        adicionar(f"🐾 {len(convocados)} convocação(ões) encontrada(s):")

        for c in convocados:
            print("=" * 50)
            print(f"Nome : {c['nome']}")
            print(f"Cargo: {c['cargo']}")
            print(f"Tipo : {c['tipo']}")
            print("=" * 50)

            adicionar(f"• {c['nome']} ({c['cargo']})")

    elif resultados:

        print(f"\n⚠️ {len(resultados)} ocorrência(s) encontrada(s).\n")
        adicionar(f"⚠️ {len(resultados)} ocorrência(s) relacionada(s).")

        for r in resultados:
            print("\nCargo:", r["cargo"])
            print("Termos:", ", ".join(r["termos"]))
            print("\nTrecho:\n")
            print(r["trecho"])
            print("\n" + "-" * 60)

    else:

        print("\n✅ Nenhuma convocação encontrada.")
        adicionar("✅ Nenhuma convocação encontrada.")

    if nomes:

        print(f"\n👤 {len(nomes)} nome(s) monitorado(s) encontrado(s).")
        adicionar(f"👤 {len(nomes)} nome(s) monitorado(s):")

        for n in nomes:
            print("\nNome:", n["nome"])
            print("\nTrecho:\n")
            print(n["trecho"])
            print("\n" + "-" * 60)

            adicionar(f"• {n['nome']}")

    else:

        print("\n👤 Nenhum nome monitorado encontrado.")
        adicionar("👤 Nenhum nome monitorado encontrado.")

    adicionar("")

    salvar_resultado(
        cidade,
        resultados,
        nomes,
        numero,
        data
    )

    atualizar_edicao(cidade, numero)