_mensagens = []


def limpar():
    _mensagens.clear()


def adicionar(texto):
    _mensagens.append(texto)


def obter():
    return "\n".join(_mensagens)