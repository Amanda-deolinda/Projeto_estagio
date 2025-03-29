import requests
from bs4 import BeautifulSoup
import os
import zipfile
import re
from glob import glob
import tabula
import pandas as pd

# Configurações
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
pasta_downloads = 'pdfs_ans'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Criar pasta de downloads
os.makedirs(pasta_downloads, exist_ok=True)

# Acessar a página
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar todos os links para PDFs
pdf_links = []
for link in soup.find_all('a', class_='internal-link'):
    href = link.get('href')
    if href and href.lower().endswith('.pdf') and 'anexo' in href.lower():
        titulo = link.text.strip() or 'arquivo_sem_nome'
        pdf_links.append((titulo, href))

# Função para limpar o nome do arquivo
def limpar_nome_arquivo(nome):
    nome = nome[:60]  # Limitar tamanho
    nome = nome.replace('/', '_').replace('\\', '_').replace(' ', '_')  # Substituir caracteres problemáticos
    nome = re.sub(r'\.+', '.', nome)  # Remover múltiplos pontos seguidos
    nome = re.sub(r'[^a-zA-Z0-9_.-]', '', nome)  # Manter apenas caracteres seguros
    return nome

# Baixar os PDFs
for titulo, link in pdf_links:
    try:
        resposta_pdf = requests.get(link, headers=headers)
        if resposta_pdf.status_code == 200:
            nome_arquivo = limpar_nome_arquivo(titulo) + "pdf"
            caminho_completo = os.path.join(pasta_downloads, nome_arquivo)
            
            with open(caminho_completo, 'wb') as f:
                f.write(resposta_pdf.content)
            print(f'Baixado: {nome_arquivo}')
        else:
            print(f'Erro ao baixar {link} - Status: {resposta_pdf.status_code}')
    except Exception as e:
        print(f'Erro no download de {link}: {str(e)}')

# Criar arquivo ZIP
def criar_zip():
    zip_path = os.path.join(os.getcwd(), 'anexos_gov.zip')
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for pdf_file in glob(os.path.join(pasta_downloads, '*.pdf')):
            zipf.write(pdf_file, arcname=os.path.basename(pdf_file))
    
    print(f'\nZIP criado com sucesso: {zip_path}')
    return zip_path

# Executar após o download
if pdf_links:
    criar_zip()
else:
    print("Nenhum PDF foi baixado.")


# Configurações
pdf_path = os.path.join("pdfs_ans", "Anexo_I.pdf")  # Ajuste o nome do arquivo corretamente
output_csv = "rol_procedimentos.csv"

# Verifica se o PDF existe
if not os.path.exists(pdf_path):
    print(f"Erro: O arquivo {pdf_path} não foi encontrado!")
    exit()

print("Extraindo tabelas do PDF...")

# Extração de todas as tabelas do PDF
dfs = tabula.read_pdf(
    pdf_path,
    pages="all",  # Todas as páginas
    multiple_tables=True,
    lattice=True,  # Usa grade para detectar tabelas corretamente
    pandas_options={'header': None},  # Não assume cabeçalhos
    encoding="utf-8"
)

# Verifica se alguma tabela foi extraída
if not dfs:
    print("Erro: Nenhuma tabela foi extraída do PDF.")
    exit()

# Concatenar todas as tabelas extraídas
full_df = pd.concat(dfs, ignore_index=True)

# Remover colunas completamente vazias
full_df.dropna(how="all", axis=1, inplace=True)

# Remover linhas completamente vazias
full_df.dropna(how="all", inplace=True)

# Definir cabeçalhos corretos (ajuste conforme a estrutura do seu PDF)
headers = [
    "PROCEDIMENTO", "RN (alteração)", "VIGÊNCIA", "SEG. ODONTOLÓGICA", "SEG. AMBULATORIAL", "HCO", 
    "HSO", "REF", "PAC", "DUT", "SUBGRUPO", "GRUPO", "CAPÍTULO"
]

# Ajustar número de colunas se necessário
num_cols = full_df.shape[1]
headers = headers[:num_cols]  # Corta cabeçalhos extras, se houver
full_df.columns = headers

# Remover linhas que repetem o cabeçalho
full_df = full_df[full_df["PROCEDIMENTO"] != "PROCEDIMENTO"]

# Salvar em CSV
full_df.to_csv(output_csv, index=False, sep=";", encoding="utf-8-sig")

print(f"✅ Dados extraídos e salvos em: {output_csv}")
# Definir nome do CSV e do ZIP
csv_file = "rol_procedimentos.csv"
zip_file = f"TESTE_Amanda.zip"  # Substitua 'Amanda' pelo seu nome, se necessário

# Verifica se o CSV existe
if not os.path.exists(csv_file):
    print(f"Erro: O arquivo {csv_file} não foi encontrado!")
    exit()

# Criar o arquivo ZIP
with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_file, arcname=os.path.basename(csv_file))

print(f"✅ Arquivo ZIP criado com sucesso: {zip_file}")