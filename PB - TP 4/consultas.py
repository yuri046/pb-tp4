import json
import sqlite3

import pandas as pd

conn = sqlite3.connect('bd.db')
cursor = conn.cursor()

#1. Trazer a média dos salários (atual) dos funcionários responsáveis por projetos concluídos, agrupados 
#por departamento.

cursor.execute('''
SELECT AVG(f.salario) as 'Média salarial', d.nome_departamento
               FROM funcionarios as f
               JOIN projetos p ON f.id_funcionario = p.funcionario_responsavel
               JOIN departamentos d ON f.id_departamento = d.id_departamento
               WHERE p.status = 'Concluido'
               GROUP BY d.id_departamento;
''')

resultado = cursor.fetchall()
print('CONSULTA 1')
for linha in resultado:
    print(linha)


#2. Identificar os três recursos materiais mais usados nos projetos, listando a descrição do recurso 
#e a quantidade total usada

cursor.execute('''
SELECT tipo_recurso,descricao_recurso, quantidade_utilizada
               FROM recursos_projeto
               ORDER BY quantidade_utilizada DESC
               LIMIT 3;
''')

resultado = cursor.fetchall()
print('CONSULTA 2')
for linha in resultado:
    print(linha)

colunas = [desc[0] for desc in cursor.description]

resultados = []
for linha in resultado:
    registro = dict(zip(colunas,linha))
    resultados.append(registro)

resultado_json = json.dumps(resultados, ensure_ascii=False, indent=4)
with open('recursos_materiais_mais_utilizados.json', mode='w', encoding='utf-8') as f:
    f.write(resultado_json)



#3. Calcular o custo total dos projetos por departamento, considerando apenas os projetos 
#'Concluídos'

cursor.execute('''
SELECT d.nome_departamento, p.custo
               FROM projetos p 
               JOIN recursos_projeto rp ON p.id_projeto = rp.id_projeto
               JOIN funcionarios f ON p.funcionario_responsavel = f.id_funcionario
               JOIN departamentos d ON f.id_departamento = d.id_departamento
               WHERE status = 'Concluido'
               GROUP BY d.nome_departamento;
''')

resultado = cursor.fetchall()
print('CONSULTA 3')
for linha in resultado:
    print(linha)

colunas = [desc[0] for desc in cursor.description]

resultados = []
for linha in resultado:
    registro = dict(zip(colunas,linha))
    resultados.append(registro)

resultado_json = json.dumps(resultados, ensure_ascii=False, indent=4)
with open('custo_total_dos_projetos_concluidos.json', mode='w', encoding='utf-8') as f:
    f.write(resultado_json)


#4. Listar todos os projetos com seus respectivos nomes, custo, data de início, data de conclusão 
#e o nome do funcionário responsável, que estejam 'Em Execução'.

cursor.execute('''
SELECT nome_projeto,custo,data_inicio,data_conclusao,funcionario_responsavel 
               FROM projetos
               WHERE status = 'Em andamento'
''')

resultado = cursor.fetchall()
print('CONSULTA 4')
for linha in resultado:
    print(linha)

colunas = [desc[0] for desc in cursor.description]

resultados = []
for linha in resultado:
    registro = dict(zip(colunas,linha))
    resultados.append(registro)

resultado_json = json.dumps(resultados, ensure_ascii=False, indent=4)
with open('projeto_em_execucao.json', mode='w', encoding='utf-8') as f:
    f.write(resultado_json)

print(resultados)


#5. Identificar o projeto com o maior número de dependentes envolvidos, considerando que os 
#dependentes são associados aos funcionários que estão gerenciando os projetos.

cursor.execute('''
SELECT p.nome_projeto, p.funcionario_responsavel, COUNT(d.id_dependente) AS 'numero_dependentes'
               FROM funcionarios f
               JOIN projetos p ON f.id_funcionario = p.funcionario_responsavel
               JOIN dependentes d ON f.id_funcionario = d.id_funcionario
               GROUP BY p.nome_projeto, p.funcionario_responsavel
               ORDER BY COUNT(d.id_dependente) DESC
               LIMIT 1
''')

resultado = cursor.fetchall()
print('CONSULTA 5')
for linha in resultado:
    print(linha)

