import csv
import json
import sqlite3

#conecta o banco de dados
conn = sqlite3.connect('bd.db')
cursor = conn.cursor()

#Criação das tabelas

#Tabela cargos
cursor.execute('''
CREATE TABLE IF NOT EXISTS cargos (
               id_cargo INTEGER PRIMARY KEY AUTOINCREMENT,
               descricao TEXT NOT NULL,
               salario_base DECIMAL(10,2) NOT NULL,
               nivel VARCHAR(255) NOT NULL,
               horas_semana INT NOT NULL
);
''')

#Tabela departamentos
cursor.execute('''
CREATE TABLE IF NOT EXISTS departamentos(
               id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
               nome_departamento VARCHAR(255) NOT NULL
);
''')

#Tabela funcionarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS funcionarios (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_funcionario VARCHAR(255) NOT NULL,
    data_contratacao DATE NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    id_cargo INT NOT NULL,
    id_departamento INT NOT NULL,
    FOREIGN KEY (id_cargo) REFERENCES cargos(id_cargo),
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
);
''')

#Tabela dependentes
cursor.execute('''
CREATE TABLE IF NOT EXISTS dependentes(
               id_dependente INTEGER PRIMARY KEY AUTOINCREMENT,
               nome_dependente VARCHAR(255) NOT NULL,
               idade INT NOT NULL,
               genero TEXT CHECK (genero IN ('masculino', 'feminino')) NOT NULL,
               id_funcionario INT NOT NULL,
               FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);
''')

#Tabela historico_salario
cursor.execute('''
CREATE TABLE IF NOT EXISTS historico_salario(
               id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
               id_funcionario INT NOT NULL,
               data DATE NOT NULL,
               salario_recebido DECIMAL(10,2) NOT NULL,
               FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);
''')

#Tabela projetos 
cursor.execute('''
CREATE TABLE IF NOT EXISTS projetos(
               id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
               nome_projeto VARCHAR(255) NOT NULL,
               descricao TEXT NOT NULL,
               data_inicio DATE NULL,
               data_conclusao DATE NULL,
               funcionario_responsavel INT NOT NULL,
               custo DECIMAL(10,2) NULL,
               status TEXT CHECK(status IN ('Em planejamento', 'Em andamento', 'Concluido', 'Cancelado')) NOT NULL,
               FOREIGN KEY (funcionario_responsavel) REFERENCES funcionarios(id_funcionario)
);
''')

#tABELA recursos do projeto
cursor.execute('''
CREATE TABLE IF NOT EXISTS recursos_projeto(
               id_recurso INTEGER PRIMARY KEY AUTOINCREMENT,
               id_projeto INT NOT NULL,
               descricao_recurso TEXT NOT NULL,
               tipo_recurso VARCHAR(100) NOT NULL,
               quantidade_utilizada DECIMAL(10,2)
)
''')

#Inserindo dados

#Tabela cargos
with open('cargo.csv', mode='r', encoding='utf-8') as cargos_csv:
    cargos = csv.DictReader(cargos_csv)

    for linha in cargos:
        cursor.execute('''INSERT INTO cargos(id_cargo, descricao, salario_base, nivel, horas_semana)
                       VALUES(:id_cargo, :descricao, :salario_base, :nivel, :horas_semana)''',linha)
        
#tabela departamentos
with open('departamento.csv', mode='r', encoding='utf-8') as departamento_csv:
    departamento = csv.DictReader(departamento_csv)

    for linha in departamento:
        cursor.execute('''INSERT INTO departamentos(id_departamento, nome_departamento)
                       VALUES(:id_departamento, :nome_departamento)''',linha)
        
#tabela funcionarios
with open('funcionarios.csv', mode='r', encoding='utf-8') as funcionarios_csv:
    funcionarios = csv.DictReader(funcionarios_csv)

    for linha in funcionarios:
        cursor.execute('''INSERT INTO funcionarios(id_funcionario, nome_funcionario, data_contratacao, salario, id_cargo, id_departamento)
                       VALUES(:id_funcionario, :nome_funcionario, :data_contratacao, :salario, :id_cargo, :id_departamento)''',linha)
        
        
#tabela dependentes
with open('dependente.csv', mode='r', encoding='utf-8') as dependentes_csv:
    depentendes = csv.DictReader(dependentes_csv)

    for linha in depentendes:
        cursor.execute('''INSERT INTO dependentes (id_dependente, nome_dependente, idade, genero, id_funcionario)
                       VALUES(:id_dependente, :nome_dependente, :idade, :genero, :id_funcionario)''',linha)
        
#tabela historico de salario
with open('historico_salario.csv', mode='r', encoding='utf-8') as historico_csv:
    historico = csv.DictReader(historico_csv)

    for linha in historico:
        cursor.execute('''INSERT INTO historico_salario(id_historico, id_funcionario, data, salario_recebido)
                       VALUES (:id_historico, :id_funcionario, :data, :salario_recebido)''',linha)
        
#tabela projeto
with open('projeto.csv', mode='r', encoding='utf-8') as projetos_csv:
    projetos = csv.DictReader(projetos_csv)

    for linha in projetos:
        cursor.execute('''INSERT INTO projetos(id_projeto,nome_projeto,descricao,data_inicio,data_conclusao,funcionario_responsavel,custo,status)
                       VALUES (:id_projeto,:nome_projeto,:descricao,:data_inicio,:data_conclusao,:funcionario_responsavel,:custo,:status)''',linha)

#tabela recursos
with open('recursos_projeto.csv', mode='r', encoding='utf-8') as recursos_csv:
    recursos = csv.DictReader(recursos_csv)

    for linha in recursos:
        cursor.execute('''INSERT INTO recursos_projeto(id_recurso,id_projeto,descricao_recurso,tipo_recurso,quantidade_utilizada)
                       VALUES(:id_recurso,:id_projeto,:descricao_recurso,:tipo_recurso,:quantidade_utilizada)''',linha)


conn.commit()
conn.close()

