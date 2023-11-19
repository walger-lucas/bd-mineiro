from query import runQuery
from database import isRunning,database
from table import Table
import glob
import pandas as pd

#pessoas = Table('Pessoas')
#pessoas.add_column('Nome')
#pessoas.add_column('Idade')
#pessoas.add_instance(["Gilmar",43])
#pessoas.add_instance(["Ana",29])
#pessoas.add_instance(["Gabriela",12])
#pessoas.add_instance(["Vandro",25])
#pessoas.add_instance(["Leia",56])
#pessoas.add_instance(["Julia",35])
#database.append(pessoas)
#carro = Table('Carro')
#carro.add_column('Cor')
#carro.add_column('Idade')
#carro.add_instance(["Toyota",29])
#carro.add_instance(["Mitono",35])
#database.append(carro)
files = glob.glob("./*.csv")
for filename in files:
    
    # reading content of csv file
    # content.append(filename)
    name = filename[2:len(filename)-4]
    tabela = Table(name)
    df = pd.read_csv(filename, index_col=None)
    for col in df.columns:
        tabela.add_column(col.strip(" '\""))
    for i in range(len(df)):
        tabela.add_instance(df.loc[i])
    database.append(tabela)
    
  
#with open('pessoas.csv', newline='') as csvfile:
    #for file in csvfile:
#        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#        for row in spamreader:
#            print(row)

running:bool = True
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
    except ValueError as e:
        print(e)

