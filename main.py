from query import runQuery
from database import isRunning,database
from table import Table
import glob
import pandas as pd

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
        inst = []
        for j in range(len(df.loc[i])):
            if type(df.loc[i][j]) == str:
                aux = df.loc[i][j]
                aux = aux[1:len(aux)-1]
                inst.append(aux)
            else:
                inst.append(df.loc[i][j])
        tabela.add_instance(inst)
    database.append(tabela)
    
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

