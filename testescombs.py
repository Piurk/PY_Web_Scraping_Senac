import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

url= "https://www.pr.senac.br/psg_novo/partials/vagas/index.asp"

requrl = requests.get(url)
soup = BeautifulSoup(requrl.text, "html.parser")
a = soup.find_all("a")

unidade = a[91].get_text(strip=True)

# Retorna Unidade Curitiba

#criação de formula para armazenar "tc" em vars

# 92 = min, 142 max
## CRIAÇÃO DO FOR
tc = []
n = 92

while n <= 142:
    teste = a[n]
    href_string = str(teste['href'])
    numero = re.search(r'tc=(\d+)', href_string).group(1)
    x = n
    tc.append(numero)
    n += 1

# Começa do 0 vai até 50

tstcid = []
m = 0

idtc = str(tc[m])
urltest = "https://www.pr.senac.br/cursos/?uep=1&tc="+idtc 
tstcodurl= BeautifulSoup(requests.get(urltest).text, "html.parser")
tstcoda = tstcodurl.find_all("a", target="_blank")
tstc = tstcoda[6]
href_string2 = str(tstc['href'])
tstcnumero = re.search(r'tstcod=(\d+)', href_string2).group(1)
tstcid.append(tstcnumero)

