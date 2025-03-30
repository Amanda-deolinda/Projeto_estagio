Este repositório contém a implementação de um teste técnico para estágio em Engenharia de Software, abordando os seguintes desafios:

🖥️ 1. Web Scraping

Acesso ao site da ANS: [Link]

Download automático dos Anexos I e II (PDFs)

Compactação dos arquivos baixados em um único .zip

📊 2. Transformação de Dados

Extração dos dados da tabela "Rol de Procedimentos e Eventos em Saúde" (Anexo I)

Estruturação e armazenamento dos dados em um arquivo .csv

Substituição das abreviações das colunas OD e AMB pelas descrições completas

Compactação do .csv no arquivo Teste_Amanda.zip

🗄️ 3. Banco de Dados

Download e preparação de dados públicos da ANS (últimos 2 anos)

Criação de tabelas para armazenamento dos dados no MySQL ou PostgreSQL

Importação dos arquivos CSV para o banco de dados

Consultas analíticas para identificar as 10 operadoras com maiores despesas médicas hospitalares no último trimestre e no último ano

🌐 4. API
Além disso, desenvolvi uma interface web utilizando Vue.js, que interage com um servidor Python para realizar as seguintes tarefas:

Tarefas de Preparação: Utilização do CSV mencionado no item 3.2.

Tarefas de Código:

Criação de uma rota no servidor que realiza uma busca textual na lista de cadastros de operadoras e retorna os registros mais relevantes.

Elaboração de uma coleção no Postman para demonstrar os resultados de forma prática.

📌 Observação: Este repositório é um projeto de teste técnico e não deve ser utilizado para outros fins sem autorização.
















