import requests # Para requisições do site
import pandas as pd # Para montar as tabelas (não utilizado nesse arquivos)
from bs4 import BeautifulSoup # Para  poder manipular os dados dos sites 
import re # Para poder cortar coisas desnecessárias do texto
from unidecode import unidecode # Para poder ajustar o texto em algumas requisições

# TESTE COM BS INICIO
url= "https://www.pr.senac.br/psg_novo/partials/vagas/index.asp" # Url onde tem todas as Listas de cursos do Senac

requrl = requests.get(url)
soup = BeautifulSoup(requrl.text, "html.parser")

a = soup.find_all("a") # Os dados de Nomes de Filiais e Cursos estão alocados em <a>'s

inicio = 0 # Criação de Var Inicio

# Isso é um filtro para localizar onde está Curitiba Centro (o inicio da Lista que vamos analisar)

for i, a_tag in enumerate(a):
    if "CURITIBA - CENTRO" in a_tag.get_text(strip=True):
        inicio = i + 1 # Adicionando mais um por causa se esse é o Curitiba centro, o próximo é o primeiro curso da lista
        break

#Criando uma nova lista, para passar os valores a partir do nosso começo
novalista = [] 

for i in range(inicio, len(a)):
    novalista.append(a[i])


fimfake = 0 # Criação de Fim Fake (ela vai medir apenas o final para a nova lista)

#Filtro fazendo o Unidecode limpar totalmente qualquer acento grafico (estava dando erro)
for f, novalista_tag in enumerate(novalista):
    if "CURITIBA - JARDIM BOTANICO" in unidecode(novalista_tag.get_text(strip=True)).upper():
        fimfake = f - 1 # Mesma lógica, se a var é onde tem o texto, uma a menos é a ultima entrada do nosso intervalo de dados
        break

fim = inicio + fimfake # Pequena formula básica, para poder somar o Inicio de a até o fim de novalista, totalizando em fim de procura var

# Agora nós temos duas vars Inicio e Fim, que são o tempo de intervalo que devemos percorrer

# Essa primeira fórmula armazena o valor de TC de cada curso, cortando fora o que não é necessário

tc = []
n = inicio

while n <= fim:
    teste = a[n]
    href_string = str(teste['href'])
    numero = re.search(r'tc=(\d+)', href_string).group(1)
    x = n
    tc.append(numero)
    n += 1

# Agora possuindo tc, nós podemos ir em cada site, buscar o valor de tstcod que podemos encontar ao inspecionar
# o elemento dá pagina e ver as turmas de cada curso

tstcod = []

for m in tc:
    
    urltest = ("https://www.pr.senac.br/cursos/?uep=1&tc="+m) # URL nova, m vai pegar o valor de cada digito de tc

    tstcodurl= BeautifulSoup(requests.get(urltest).text, "html.parser")
    tstcoda = tstcodurl.find_all("a",attrs={'href': lambda x: x and 'tstcod' in x}) # Esse é um pouco confuso, mas eu 
    # descobri que dentre os <a>s dessa pagina, eles não eram padronizados, as vezes um poderia estar em tstcoda[6], as vezes em 
    # tstcoda[2], por isso precisa de uma formula para pegar o <a> com tstcod

    tstcody = tstcoda[0] # como estou usando find_all seria um array então eu só passei como var
    
    href_string2 = tstcody['href']
    
    tstcnumero = re.search(r'tstcod=(\d+)', href_string2).group(1) # corte para adicionar apenas os numeros
    
    tstcod.append(tstcnumero) # números adicionados
# TESTE COM BS FIM

tamanho = len(tc)

for i in tamanho:
    completo= (f"https://www.pr.senac.br/psg/?p_psg=10&op=1&uc=1&tstcod="+tstcod[i]+"&tc="+tc[i])

print(completo)


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

# Extração de Dados em Planilha
def extrair_tabela(html_table):
    rows = html_table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all(["th", "td"])
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    return(data)

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



