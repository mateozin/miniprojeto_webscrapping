import requests
import bs4
import csv
import os

pasta_atual = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(pasta_atual, "noticias_g1.csv")
 
#utilizando o site do G1 para Web Scrapping
site = "https://g1.globo.com/"
 
resposta = requests.get(site, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
 
# interrope se o erro falhar
resposta.raise_for_status()
 
print(f"Página baixada! Status: {resposta.status_code}")

soup = bs4.BeautifulSoup(resposta.text, "html.parser")
 
noticias = []
 
for tag in soup.select("a"):
    titulo = tag.get_text(strip=True)
    link = tag.get("href", "")
 
    #seleciona apenas titulos grandes.
    if len(titulo) > 40 and link.startswith("https://g1.globo.com"):
        noticias.append({"titulo": titulo, "link": link})
 
# remove repetições
noticias = list({n["titulo"]: n for n in noticias}.values())
 
print(f"{len(noticias)} manchetes encontradas.\n")
 
#exibindo as 10 primeiras encontradas
for i, noticia in enumerate(noticias[:10], start=1):
    print(f"{i}. {noticia['titulo'][:80]}")
    print(f"   {noticia['link']}\n")
 
#salvando os resultados em um arquivo .csv
with open(arquivo, "w", newline="", encoding="utf-8") as f:
    escritor = csv.DictWriter(f, fieldnames=["titulo", "link"])
    escritor.writeheader()
    escritor.writerows(noticias)
 
print(f"Resultados salvos em '{arquivo}'!")