from modelos import ResumoExecucao

from cidades import campinas
from cidades import sorocaba
from cidades import vinhedo


def listar_cidades():

    print("Iniciando monitoramento...\n")

    resumo = ResumoExecucao()

    for modulo in (campinas, sorocaba, vinhedo):

        resultado = modulo.buscar()

        resumo.cidades.append(resultado)

        print()

    return resumo