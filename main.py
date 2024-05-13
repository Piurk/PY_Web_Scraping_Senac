import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Criação do Testcode e Filtros

#linkdeanalises = 'https://www.pr.senac.br/psg/?p_psg=10&op=1&uc=1&tstcod=3211&tc=202400610'

tc = "202400503"
tstcod = "3175"

completo= "https://www.pr.senac.br/psg/?p_psg=10&op=1&uc=1&tstcod="+tstcod+"&tc="+tc

# Extração de Dados em Planilha
def extrair_tabela(html_table):
    rows = html_table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all(["th", "td"])
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    return(data)


# Requisição do BS
req = requests.get(completo)
site = BeautifulSoup(req.text, "html.parser")
tabelastestes = site.find_all("table")

# Adicionando também dados de processo seletivo
dados_adicionais = site.find_all("h3")
dados_adicionais_str = ' '.join(str(elem) for elem in dados_adicionais)

string_html = dados_adicionais_str

nome_curso_regex = r'<b>(.*?)</b>'
nome_curso_match = re.search(nome_curso_regex, string_html)
nome_curso = nome_curso_match.group(1) if nome_curso_match else None

processo_seletivo_regex = r'Processo Seletivo: <b>(\d+)</b>'
processo_seletivo_match = re.search(processo_seletivo_regex, string_html)
processo_seletivo = processo_seletivo_match.group(1) if processo_seletivo_match else None


# Passando os dados do BS pra tabela
data = extrair_tabela(tabelastestes[1])


# Adicionar o nome do curso e o processo seletivo como uma nova coluna
nome_curso_column = ['Nome do Curso'] + [nome_curso] * (len(data))
processo_seletivo_column = ['Processo Seletivo'] + [processo_seletivo] * (len(data))

# Adicionando as novas colunas à lista de dados
for i in range(len(data)):
    data[i].insert(0, nome_curso_column[i])
    data[i].insert(1, processo_seletivo_column[i])

# Dataframe Pandas
df = pd.DataFrame(data[1:], columns=data[0])


# Para esse projeto vou fazer xlsx pois o excel é meu queridinho

df.to_excel("dados.xlsx", index=False)

# Tá funcionando a base, proximo passo é fazer isso pra TODAS as escolas de curitiba centro



