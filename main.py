from query import runQuery
from database import isRunning,database
from table import Table

pessoas = Table('Pessoas')
pessoas.add_column('Nome')
pessoas.add_column('Idade')
pessoas.add_instance(["Gilmar",43])
pessoas.add_instance(["Ana",29])
pessoas.add_instance(["Gabriela",12])
pessoas.add_instance(["Vandro",25])
pessoas.add_instance(["Leia",56])
pessoas.add_instance(["Julia",35])
database.append(pessoas)
carro = Table('Carro')
carro.add_column('Cor')
carro.add_column('Idade')
carro.add_instance(["Toyota",29])
carro.add_instance(["Mitono",35])
database.append(carro)

running = True
while(running):
    try:
        text = input()
        if(text =='sair'):
            running = False
            continue
        query = runQuery(text)
        if query:
            print()
            query.print()
            print()
    except Exception as e:
        print(e)

