from modelos import ResumoExecucao, ResultadoCidade

from cidades import campinas
from cidades import sorocaba
from cidades import vinhedo
from cidades import sumare

from resumo import adicionar


def listar_cidades():

    print("Iniciando monitoramento...\n")

    resumo = ResumoExecucao()

    for modulo in (campinas, sorocaba, vinhedo, sumare):

        try:
            resultado = modulo.buscar()

            resumo.cidades.append(resultado)

        except Exception as e:
            nome_cidade = modulo.__name__.split(".")[-1]

            print(f"❌ Erro ao processar {nome_cidade}:")
            print(type(e).__name__)
            print(e)

            resultado = ResultadoCidade(cidade=nome_cidade)
            resultado.erros.append(f"{type(e).__name__}: {e}")

            resumo.cidades.append(resultado)

            adicionar(
                f"❌ <b>{nome_cidade.capitalize()}</b>: não foi possível verificar o Diário Oficial."
            )

        print()

    return resumo