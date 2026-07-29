_mensagens = []
_tem_convocacao = False


def limpar():
    _mensagens.clear()

    global _tem_convocacao
    _tem_convocacao = False


def adicionar(texto):
    _mensagens.append(texto)


def obter():
    return "\n".join(_mensagens)


def marcar_convocacao():
    global _tem_convocacao
    _tem_convocacao = True


def tem_convocacao():
    return _tem_convocacao