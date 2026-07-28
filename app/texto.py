import re


def normalizar_texto(texto):

    # Junta palavras quebradas por hífen no fim da linha
    texto = re.sub(r"-\s*\n\s*", "", texto)

    # Remove quebras de linha
    texto = texto.replace("\n", " ")

    # Remove espaços duplicados
    texto = re.sub(r"\s+", " ", texto)

    return texto