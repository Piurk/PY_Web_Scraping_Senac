import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from unidecode import unidecode

# URL onde estão todas as listas de cursos do Senac
url = "https://www.pr.senac.br/psg_novo/partials/vagas/index.asp"

# Fazendo a requisição para obter o HTML da página
requrl = requests.get(url)
soup = BeautifulSoup(requrl.text, "html.parser")

# Encontrando todos os elementos <a> na página
a = soup.find_all("a")

# Identificando o início da lista de cursos
inicio = 0
for i, a_tag in enumerate(a):
    if "CURITIBA - CENTRO" in a_tag.get_text(strip=True):
        inicio = i + 1
        break

# Criando uma lista com os valores a partir do início identificado
novalista = [a[i] for i in range(inicio, len(a))]

# Identificando o fim da lista de cursos
fimfake = 0
for f, novalista_tag in enumerate(novalista):
    if "CURITIBA - JARDIM BOTANICO" in unidecode(novalista_tag.get_text(strip=True)).upper():
        fimfake = f - 1
        break

# Calculando o índice de fim baseado no início e no fimfake
fim = inicio + fimfake

# Extraindo os valores de TC de cada curso
tc = []

for n in range(inicio, fim + 1):
    href_string = a[n]['href']
    numero = re.search(r'tc=(\d+)', href_string).group(1)
    tc.append(numero)

# Extraindo os valores de tstcod e carga horaria para cada curso
tstcod = []
cargahoraria = []
for m in tc:
    urltest = f"https://www.pr.senac.br/cursos/?uep=1&tc={m}"
    tstcoda_url = BeautifulSoup(requests.get(urltest).text, "html.parser")
    tstcoda = tstcoda_url.find_all("a", attrs={'href': lambda x: x and 'tstcod' in x})
    if tstcoda:
        href_string2 = tstcoda[0]['href']
        tstcnumero = re.search(r'tstcod=(\d+)', href_string2).group(1)
        tstcod.append(tstcnumero)
    

# Extraindo dados das tabelas para cada URL construída
all_data = []
for r, tst in enumerate(tstcod):
    completo = f"https://www.pr.senac.br/psg/?p_psg=10&op=1&uc=1&tstcod={tst}&tc={tc[r]}"
    req = requests.get(completo)
    site = BeautifulSoup(req.text, "html.parser")
    tabelastestes = site.find_all("table", class_="table table-bordered table-striped table-responsive")
    
    if not tabelastestes:
        print(f"Tabela não encontrada para o curso {tc[r]}")
        continue
    
    

    # Extraindo dados adicionais como nome do curso e processo seletivo
    dados_adicionais = site.find_all("h3")
    dados_adicionais_str = ' '.join(str(elem) for elem in dados_adicionais)
    


    nome_curso_match = re.search(r'<b>(.*?)</b>', dados_adicionais_str)
    nome_curso = nome_curso_match.group(1) if nome_curso_match else "N/A"
    
    processo_seletivo_match = re.search(r'Processo Seletivo: <b>(\d+)</b>', dados_adicionais_str)
    processo_seletivo = processo_seletivo_match.group(1) if processo_seletivo_match else "N/A"
    
    # Função para extrair dados da tabela HTML
    def extrair_tabela(html_table):
        rows = html_table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all(["th", "td"])
            cols = [col.text.strip() for col in cols]
            data.append(cols)
        return data
    
    # Extraindo dados da tabela
    data = extrair_tabela(tabelastestes[0])
    
    # Adicionando o nome do curso e o processo seletivo como novas colunas
    for row in data[1:]:  # Excluindo o cabeçalho
        row.insert(0, nome_curso)
        row.insert(1, processo_seletivo)
    
    all_data.extend(data[1:])  # Adicionando dados (sem o cabeçalho) à lista total

# Cabeçalhos para o DataFrame
headers = ['Nome do Curso', 'Processo Seletivo'] + data[0]

# Criando o DataFrame e salvando em Excel
df = pd.DataFrame(all_data, columns=headers)
df.to_excel("dados.xlsx", index=False)

print("Dados extraídos e salvos com sucesso!")