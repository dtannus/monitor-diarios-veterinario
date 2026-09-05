from datetime import datetime
import sys
import traceback

from logger import registrar
from buscador import listar_cidades
from cidades import campinas, sorocaba, vinhedo, sumare, itupeva
from telegram import enviar_mensagem
from resumo import limpar, obter, tem_convocacao


def iniciar_monitor():

    inicio = datetime.now()

    registrar("=" * 50)
    registrar("MONITOR DE DIÁRIOS OFICIAIS")
    registrar("=" * 50)
    registrar(f"Início: {inicio.strftime('%d/%m/%Y %H:%M:%S')}")

    limpar()

    try:

        enviar_mensagem(
            f"🚀 <b>Monitor iniciado</b>\n\n"
            f"🗓 {inicio.strftime('%d/%m/%Y')}\n"
            f"🕕 {inicio.strftime('%H:%M:%S')}"
        )

        if len(sys.argv) >= 4 and sys.argv[1] == "--teste":

            cidade = sys.argv[2].lower()
            numero = sys.argv[3]

            print(f"\nModo de teste - {cidade.capitalize()} - edição {numero}\n")

            if cidade == "campinas":
                campinas.testar_edicao(numero)

            elif cidade == "sorocaba":
                sorocaba.testar_edicao(numero)

            elif cidade == "vinhedo":
                vinhedo.testar_edicao(numero)

            elif cidade == "sumare":
                sumare.testar_edicao(numero)
              
            elif cidade == "itupeva":
                itupeva.testar_edicao(numero)

            else:
                print(f"❌ Cidade '{cidade}' não cadastrada.")

        else:

            listar_cidades()

        resumo = obter().strip()

        if resumo:

            if tem_convocacao():
                cabecalho = (
                    "⚠️ <b>Foram encontradas convocações para "
                    "Médico Veterinário.</b>\n\n"
                )
            else:
                cabecalho = (
                    "ℹ️ <b>Nenhuma convocação para Médico Veterinário "
                    "foi encontrada nesta execução.</b>\n\n"
                )

            enviar_mensagem(
                "<b>📋 Resumo da execução</b>\n\n"
                f"{cabecalho}"
                f"{resumo}"
            )

        else:

            enviar_mensagem(
                "<b>📋 Resumo da execução</b>\n\n"
                "ℹ️ <b>Nenhuma edição nova foi encontrada para análise.</b>"
            )

        fim = datetime.now()
        duracao = fim - inicio

        enviar_mensagem(
            f"✅ <b>Monitor concluído</b>\n\n"
            f"🗓 {fim.strftime('%d/%m/%Y')}\n"
            f"🕕 {fim.strftime('%H:%M:%S')}\n"
            f"⏱ Tempo de execução: {duracao}"
        )

    except Exception as erro:

        traceback.print_exc()

        enviar_mensagem(
            f"❌ <b>Erro durante a execução do monitor</b>\n\n"
            f"<b>Erro:</b>\n"
            f"<code>{erro}</code>"
        )

        raise


if __name__ == "__main__":
    iniciar_monitor()