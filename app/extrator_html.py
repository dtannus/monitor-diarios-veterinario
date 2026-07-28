from bs4 import BeautifulSoup


def obter_links(html):
    soup = BeautifulSoup(html, "html.parser")

    links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]

        if href:
            links.append(href)

    return links