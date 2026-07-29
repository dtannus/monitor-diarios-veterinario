from modelos import ResumoExecucao

from cidades import campinas
from cidades import sorocaba
from cidades import vinhedo
from cidades import sumare


def listar_cidades():

    print("Iniciando monitoramento...\n")

    resumo = ResumoExecucao()

    for modulo in (campinas, sorocaba, vinhedo, sumare):

        resultado = modulo.buscar()

        resumo.cidades.append(resultado)

        print()

    return resumo