from pypdf import PdfReader
from io import BytesIO


def extrair_texto(pdf):
    texto = ""

    try:
        if isinstance(pdf, bytes):
            leitor = PdfReader(BytesIO(pdf))
        else:
            leitor = PdfReader(pdf)

        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""

        return texto

    except Exception as erro:
        print("Erro ao ler PDF:")
        print(erro)
        return None