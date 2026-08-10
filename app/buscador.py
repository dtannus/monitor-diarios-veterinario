from modelos import ResumoExecucao, ResultadoCidade

from cidades import campinas
from cidades import sorocaba
from cidades import vinhedo
from cidades import sumare

from resumo import adicionar
from logger import registrar


def listar_cidades():

    registrar("Iniciando monitoramento...")

    resumo = ResumoExecucao()

    for modulo in (campinas, sorocaba, vinhedo, sumare):

        try:
            resultado = modulo.buscar()

            resumo.cidades.append(resultado)

        except BaseException as e:

            registrar("Entrou no except do buscador.")

            nome_cidade = modulo.__name__.split(".")[-1]

            registrar(f"❌ Erro ao processar {nome_cidade}:")
            registrar(type(e).__name__)
            registrar(e)

            resultado = ResultadoCidade(cidade=nome_cidade)
            resultado.erros.append(f"{type(e).__name__}: {e}")

            resumo.cidades.append(resultado)

            adicionar(
                f"❌ <b>{nome_cidade.capitalize()}</b>: não foi possível verificar o Diário Oficial."
            )

        registrar("")

    return resumo