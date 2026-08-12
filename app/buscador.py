from cidades import campinas
from cidades import sorocaba
from cidades import vinhedo
from cidades import sumare

from resumo import adicionar
from logger import registrar


def listar_cidades():
    registrar("Iniciando monitoramento...")

    cidades = (
        campinas,
        sorocaba,
        vinhedo,
        sumare,
    )

    for modulo in cidades:
        nome_cidade = modulo.__name__.split(".")[-1]

        try:
            modulo.buscar()

        except Exception as erro:
            registrar(f"❌ Erro ao processar {nome_cidade}:")
            registrar(type(erro).__name__)
            registrar(erro)

            adicionar(
                f"❌ <b>{nome_cidade.capitalize()}</b>: "
                "não foi possível verificar o Diário Oficial."
            )

        registrar("")