# Projeto de Automação com WebScraping Senac

Este documento descreve o projeto de automação desenvolvido para gerar tabelas Excel de forma automatizada. O objetivo é automatizar o serviço de consultas a web realizada no Senac.

## Objetivo

O principal objetivo deste projeto é criar um sistema automatizado que possa:

- Gerar uma tabela Excel com informações sobre os cursos.
- Reduzir o número de passos para chegar na lista de aprovação.
- Ser possível atualização em tempo real graças ao WebScraping.

## Funcionalidades

O sistema de automação de geração de tabelas Excel inclui as seguintes funcionalidades principais:

1. **Importação de Dados**: O sistema atraves do uso do Beautiful Soup consegue importar dados dos arquivos HTML  do Senac.

2. **Limpeza de Dados**: Alguns dos arquivos vem muito poluídos por isso a biblioteca Re permite ajustar.

3. **Geração de Tabelas**: Formatação de tabelas com dados importados e polidos

4. **Exportação de Tabelas**: Uma vez gerada a tabela, o sistema pode exportá-la para um arquivo Excel (.xlsx) pronto para uso.

## Tecnologias Utilizadas

O projeto faz uso das seguintes tecnologias:

- **Linguagem de Programação**: Python é a linguagem principal para o desenvolvimento do sistema de automação, devido à sua facilidade de uso e à disponibilidade de bibliotecas como pandas e openpyxl.
  
- **Bibliotecas Python**:
  - *pandas*: Utilizada para manipulação de dados.
  - *openpyxl*: Utilizada para interação com arquivos Excel.
  - *BeautifulSoup*: Utilizada para a parte de Webscraping do site.
  - *requests*: Utilizada para fazer requisições ao site.
  - *re*: Para ajuste de caracteres no texto.

## Fluxo de Trabalho

O fluxo de trabalho típico do sistema de automação de geração da tabela Excel é o seguinte:

1. **Importação de Dados**: Os dados são importados do arquivo HTML do Site do Senac, atraves do Beautiful Soup.

2. **Calibre**: Para determinar quais tabelas correspondem a quais alunos, é necessário uma serie de filtragens para conseguir as variaveis correspondentes para pegar todos os dados

3. **Geração de Tabela**: Com base nos dados manipulados, a tabela Excel é gerada, com cabeçalhos, colunas e linhas apropriadas.

4. **Exportação da Tabela**: A tabela final é exportada para um arquivo Excel (.xlsx), pronto para uso.

## Conclusão

No momento, o serviço não se encontra completo, mas está sendo divertido montar

## Equipe 

**Integrantes: **

- Daniel Dias Ribeiro
- Elaine Gomes e Silva
- João Pedro Piurkoski
- Michael Klug Berger Costa
- Robson Allan Viana

**Orientados por: **

Carlos Eduardo Lopes
Roger Lucio de Lima Bassan

