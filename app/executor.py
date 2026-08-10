from logger import registrar
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

    registrar("\n========================================")
    registrar(f"{cidade} - Edição {numero} - {data}")
    registrar("========================================")

    adicionar(f"📍 <b>{cidade}</b>")
    adicionar(f"📰 Edição {numero} - {data}")

    registrar(f"URL do PDF: {url_pdf}")
    registrar("Baixando PDF...")

    pdf = baixar_pdf(url_pdf)

    if not pdf:
        registrar("❌ Erro ao baixar PDF.")
        adicionar("❌ Erro ao baixar PDF.")
        adicionar("")
        return

    registrar("Extraindo texto...")

    texto = extrair_texto(pdf)

    if not texto:
        registrar("❌ Não foi possível extrair o texto.")
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

        registrar(f"\n🐾 {len(convocados)} convocado(s) encontrado(s).\n")
        adicionar(f"🐾 {len(convocados)} convocação(ões) encontrada(s):")

        for c in convocados:
            registrar("=" * 50)
            registrar(f"Nome : {c['nome']}")
            registrar(f"Cargo: {c['cargo']}")
            registrar(f"Tipo : {c['tipo']}")
            registrar("=" * 50)

            adicionar(f"• {c['nome']} ({c['cargo']})")

    elif resultados:

        registrar(f"\n⚠️ {len(resultados)} ocorrência(s) encontrada(s).\n")
        adicionar(f"⚠️ {len(resultados)} ocorrência(s) relacionada(s).")

        for r in resultados:
            registrar("Cargo:", r["cargo"])
            registrar("Termos:", ", ".join(r["termos"]))
            registrar("\nTrecho:\n")
            registrar(r["trecho"])
            registrar("\n" + "-" * 60)

    else:

        registrar("\n✅ Nenhuma convocação encontrada.")
        adicionar("✅ Nenhuma convocação encontrada.")

    if nomes:

        registrar(f"\n👤 {len(nomes)} nome(s) monitorado(s) encontrado(s).")
        adicionar(f"👤 {len(nomes)} nome(s) monitorado(s):")

        for n in nomes:
            registrar("Nome:", n["nome"])
            registrar("\nTrecho:\n")
            registrar(n["trecho"])
            registrar("\n" + "-" * 60)

            adicionar(f"• {n['nome']}")

    else:

        registrar("\n👤 Nenhum nome monitorado encontrado.")
        adicionar("👤 Nenhum nome monitorado encontrado.")

    adicionar("")

    salvar_resultado(
        cidade,
        resultados,
        nomes,
        numero,
        data
    )

    registrar(f"Atualizando controle: {cidade} -> edição {numero}")

    atualizar_edicao(cidade, numero)

    registrar(f"Controle atualizado com sucesso: {cidade} -> edição {numero}")