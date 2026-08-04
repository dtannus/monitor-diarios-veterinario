import re


def chave_edicao(edicao):
    """
    Converte uma edição em uma chave comparável.

    Exemplos:
        2189     -> (2189, "")
        "2189"   -> (2189, "")
        "2189-A" -> (2189, "A")
        "2189-B" -> (2189, "B")
    """

    if edicao is None:
        return (-1, "")

    texto = str(edicao).strip().upper()

    match = re.match(r"(\d+)(?:-([A-Z]+))?$", texto)

    if not match:
        return (-1, texto)

    numero = int(match.group(1))
    sufixo = match.group(2) or ""

    return (numero, sufixo)
    
def edicao_maior(atual, ultima):
    """
    Retorna True se a edição atual for mais recente que a última.
    """

    return chave_edicao(atual) > chave_edicao(ultima)
    
def chave_ordenacao(edicao):
    """
    Retorna a chave usada para ordenar edições.
    """
    return chave_edicao(edicao)