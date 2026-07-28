import requests

def baixar_arquivo(url, destino):
    resposta = requests.get(url, stream=True, timeout=30)
    resposta.raise_for_status()

    with open(destino, "wb") as arquivo:
        for bloco in resposta.iter_content(8192):
            if bloco:
                arquivo.write(bloco)

    return destino