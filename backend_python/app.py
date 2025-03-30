from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Carregar CSV tratando quebras de linha
df = pd.read_csv(
    'Relatorio_cadop.csv',
    sep=';',
    encoding='utf-8',
    quotechar='"',
    dtype=str,
    na_filter=False,
    engine='python',  # Usa engine Python para melhor tratamento de quebras
    on_bad_lines='warn'  # Avisa sobre linhas malformadas sem interromper
)


# Renomear colunas manualmente (garantindo alinhamento)
df = df.rename(columns={
    df.columns[0]: 'Registro_ANS',
    df.columns[1]: 'CNPJ',
    df.columns[2]: 'Razao_Social',
    df.columns[3]: 'Nome_Fantasia',
    df.columns[4]: 'Modalidade',
    df.columns[5]: 'Logradouro',
    df.columns[6]: 'Numero',
    df.columns[7]: 'Complemento',
    df.columns[8]: 'Bairro',
    df.columns[9]: 'Cidade',
    df.columns[10]: 'UF',
    df.columns[11]: 'CEP',
    df.columns[12]: 'DDD',
    df.columns[13]: 'Telefone',
    df.columns[14]: 'Fax',
    df.columns[15]: 'Endereco_eletronico',
    df.columns[16]: 'Representante',
    df.columns[17]: 'Cargo_Representante',
    df.columns[18]: 'Regiao_de_Comercializacao',
    df.columns[19]: 'Data_Registro_ANS'
})

# Limpeza agressiva de quebras de linha
df = df.apply(lambda x: x.replace('\n', '').strip() if isinstance(x, str) else x)

# Verificar estrutura
print("\nExemplo de dados após correção:")
print(df[['Registro_ANS', 'Data_Registro_ANS']].head(3).to_string(index=False))

operadoras = df.to_dict('records')

@app.route('/')
def home():
    return 'Bem-vindo ao meu projeto!'


@app.route('/search')
def search():
    query = request.args.get('q', '').lower().strip()
    resultados = []
    for op in operadoras:
        if query in op['Registro_ANS'].lower() or query in op['Razao_Social'].lower() or query in op['Nome_Fantasia'].lower():
            resultados.append(op)
    return jsonify(resultados[:50])

if __name__ == '__main__':
    app.run(debug=True)