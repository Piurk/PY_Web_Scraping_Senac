import requests # Para requisições do site
import pandas as pd # Para montar as tabelas (não utilizado nesse arquivos)
from bs4 import BeautifulSoup # Para  poder manipular os dados dos sites 
import re # Para poder cortar coisas desnecessárias do texto
from unidecode import unidecode # Para poder ajustar o texto em algumas requisições

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

    