import requests
import bs4
import csv
import os

pasta_atual = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(pasta_atual, "noticias_g1.csv")

#utilizando o site G1 para Web Scrapping
site = "https://g1.globo.com/"

resposta = requests.get(site, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
resposta.raise_for_status()
if resposta.status_code == 200:
    print(f"Página encontrada com sucesso! Status: {resposta.status_code}")
else:
    print(f"Falha ao encontrar página. Status: {resposta.status_code}")
soup = bs4.BeautifulSoup(resposta.text, "html.parser")

#escolher o número de caracteres para procurar
caracteres = int(input("Digite o número de caracteres mínimo da notícia: "))

noticias = []

for tag in soup.select("a"):
    titulo = tag.get_text(strip=True)
    link = tag.get("href", "")

    if len(titulo) > caracteres and link.startswith("https://g1.globo.com"):
        noticias.append({"titulo": titulo, "link": link})

noticias = list({n["titulo"]: n for n in noticias}.values())

print(f"{len(noticias)} notícias encontradas.\n")
print("[Enter] próxima | [q + Enter] cancelar\n")

if os.path.exists(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        ja_salvas = {row["titulo"] for row in csv.DictReader(f)}
else:
    ja_salvas = set()

vistas = []

for i, noticia in enumerate(noticias, start=1):
    print(f"{i}. {noticia['titulo'][:80]}")
    print(f"   {noticia['link']}\n")
    vistas.append(noticia)

    if input().strip().lower() == "q":
        print("\nCancelado pelo usuário.")
        break
    print()

novas = [n for n in vistas if n["titulo"] not in ja_salvas]

with open(arquivo, "a", newline="", encoding="utf-8") as f:
    escritor = csv.DictWriter(f, fieldnames=["titulo", "link"])
    if not ja_salvas:
        escritor.writeheader()
    escritor.writerows(novas)

print(f"{len(novas)} novas notícias salvas em '{arquivo}'!")