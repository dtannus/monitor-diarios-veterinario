from rede import baixar_pagina
from extrator_html import obter_links

url = "https://www.campinas.sp.gov.br/diario-oficial"

html = baixar_pagina(url)

links = obter_links(html)

print(f"Foram encontrados {len(links)} links.\n")

for link in links[:30]:
    print(link)