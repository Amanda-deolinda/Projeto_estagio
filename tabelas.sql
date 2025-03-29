
-- Teste de banco --


-- PARTE 1 -- 

-- CRIAÇÃO DAS TABELAS -- 
CREATE TABLE operadoras (
    Registro_ANS VARCHAR(200) NOT NULL PRIMARY KEY,
    CNPJ VARCHAR(200) NOT NULL,
    Razao_Social VARCHAR(200) NOT NULL,
    Nome_Fantasia VARCHAR(200),
    Modalidade VARCHAR(200),
    Logradouro VARCHAR(200),
    Numero VARCHAR(200),
    Complemento VARCHAR(200),
    Bairro VARCHAR(200),
    Cidade VARCHAR(200),
    UF VARCHAR(200),
    CEP VARCHAR(200),
    DDD VARCHAR(200),
    Telefone VARCHAR(200),
    Fax VARCHAR(200),
    Endereco_eletronico VARCHAR(200),
    Representante VARCHAR(200),
    Cargo_Representante VARCHAR(200),
    Regiao_de_Comercializacao INT,
    Data_Registro_ANS DATE
);

CREATE TABLE demonstrativos_contabeis (
    data DATE NOT NULL,                             
    reg_ans INT NOT NULL,                          
    cd_conta_contabil VARCHAR(20) NOT NULL,       
    descricao VARCHAR(255) NOT NULL,               
    vl_saldo_inicial DECIMAL(15,2) NOT NULL,       
    vl_saldo_final DECIMAL(15,2) NOT NULL          
);

-- ALTERAÇÃO DA TABELA OPERADORAS -- 
ALTER TABLE operadoras
	DROP PRIMARY KEY,
	MODIFY COLUMN Registro_ANS VARCHAR(555) NOT NULL,
	MODIFY COLUMN CNPJ VARCHAR(555) NOT NULL,
	MODIFY COLUMN Razao_Social VARCHAR(555) NOT NULL,
	MODIFY COLUMN Nome_Fantasia VARCHAR(555),
	MODIFY COLUMN Modalidade VARCHAR(255),
	MODIFY COLUMN Logradouro VARCHAR(255),
	MODIFY COLUMN Numero VARCHAR(255),
	MODIFY COLUMN Complemento VARCHAR(255),
	MODIFY COLUMN Bairro VARCHAR(255),
	MODIFY COLUMN Cidade VARCHAR(255),
	MODIFY COLUMN UF VARCHAR(255),
	MODIFY COLUMN CEP VARCHAR(255),
	MODIFY COLUMN DDD VARCHAR(255),
	MODIFY COLUMN Telefone VARCHAR(255),
	MODIFY COLUMN Fax VARCHAR(255),
	MODIFY COLUMN Endereco_eletronico VARCHAR(255),
	MODIFY COLUMN Representante VARCHAR(255),
	MODIFY COLUMN Cargo_Representante VARCHAR(255),
	MODIFY COLUMN Regiao_de_Comercializacao VARCHAR(255),
	MODIFY COLUMN Data_Registro_ANS VARCHAR(255);

-- COMANDO PARA CARREGAR CADA ARQUIVO CSV (execute um para cada arquivo)
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(Registro_ANS, CNPJ, Razao_Social, Nome_Fantasia, Modalidade, Logradouro, Numero, Complemento, Bairro, 
Cidade, UF, CEP, DDD, Telefone, Fax, Endereco_eletronico, Representante,
Cargo_Representante,
Regiao_de_Comercializacao,
Data_Registro_ANS);

-- COMANDO PARA CARREGAR CADA ARQUIVO CSV (execute um para cada arquivo)
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Registro_ANS, CNPJ, Razao_Social, Nome_Fantasia, Modalidade, Logradouro, Numero, Complemento, Bairro, 
Cidade, UF, CEP, DDD, Telefone, Fax, Endereco_eletronico, Representante,
Cargo_Representante,
Regiao_de_Comercializacao,
Data_Registro_ANS);



-- COMANDO PARA CARREGAR CADA ARQUIVO CSV (execute um para cada arquivo)
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/4T2023.csv'
INTO TABLE demonstrativos_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@data, reg_ans, cd_conta_contabil, descricao, @vl_saldo_inicial, @vl_saldo_final)
SET 
    data = STR_TO_DATE(@data, '%d/%m/%Y'),
    vl_saldo_inicial = REPLACE(@vl_saldo_inicial, ',', '.'),
    vl_saldo_final = REPLACE(@vl_saldo_final, ',', '.');
SELECT DISTINCT data FROM demonstrativos_contabeis;
select * from demonstrativos_contabeis;


-- PARTE 3 -- 

SELECT * FROM demonstrativos_contabeis;

-- ULTIMO ANO 
SELECT reg_ans, 
       SUM(vl_saldo_final) AS total_despesas
FROM demonstrativos_contabeis
WHERE YEAR(data) = YEAR(CURDATE()) - 1  -- Considera o último ano completo
GROUP BY reg_ans
ORDER BY total_despesas DESC
LIMIT 10;

-- UTIMOS TRIMESTRE 
SELECT reg_ans, 
       SUM(vl_saldo_final) AS total_despesas
FROM demonstrativos_contabeis
WHERE data >= DATE_SUB(CURDATE(), INTERVAL 7 MONTH) 
GROUP BY reg_ans
ORDER BY total_despesas DESC
LIMIT 10;

