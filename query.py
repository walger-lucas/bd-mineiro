from table import Table, TableCoordinate
from operation import Operation, createOperation, SET_OP
from separator import *
from syntax import *
from mergeSort import *
from database import exitDatabase
import glob
import pandas as pd
import mysql.connector
import csv

        
#cria instancia com as colunas dadas
def createInstance(index,columns,tables):
    instance = []
    for column in columns:
        instance.append(tables[column.table_index].getValue(column.column,index[column.table_index]))
    return instance

# executa query de select
def runSelect(columns,tables,operation:Operation,order_id,order_asc):
    new_table = Table("table")
    #adiciona as novas colunas em ordem a tabela
    for column in columns:
        new_table.add_column(tables[column.table_index].name+"_"+tables[column.table_index].columnNames[column.column])

    if tables == []:
        return None
    #inicializa indexes
    index = []
    index_size = []
    for t in tables:
        index_size.append(t.rowCount())
        index.append(0)
    
    total = index_size[0]
    for t in index_size[1:]:
        total*=t
    index_len = len(index)
    i=0
    #passa por todos os valores possiveis
    while i<total:
        if operation.value(tables,index):
            new_table.add_instance(createInstance(index,columns,tables))
        index[0]+=1
        for j in range(index_len):
            if index[j]>= index_size[j] and j+1< index_len:
                index[j]=0
                index[j+1]+=1
            else:
                break
        i+=1
    sortTable(new_table,order_id,order_asc)
    return new_table

def runDelete(delete_table_index,tables,operation:Operation):
    if tables == []:
        return
    index = []
    index_size = []
    for t in tables:
        index_size.append(t.rowCount())
        index.append(0)
    
    total = index_size[0]
    for t in index_size[1:]:
        total*=t
    index_len = len(index)
    i=0
    #passa por todos os valores possiveis e vê se devem ser deletados
    delete = [False]*tables[delete_table_index].rowCount()
    while i<total:
        if operation.value(tables,index):
            delete[index[delete_table_index]]=True
        index[0]+=1
        for j in range(index_len):
            if index[j]>= index_size[j] and j+1< index_len:
                index[j]=0
                index[j+1]+=1
            else:
                break
        i+=1
    # deleta todas as entradas marcadas
    i = tables[delete_table_index].rowCount()-1
    while i>=0:
        if delete[i] == True:
            tables[delete_table_index].rows.pop(i)
        i-=1

def runUpdate(tables,set_op,where_op):
    if tables == []:
        return
    index = []
    index_size = []
    for t in tables:
        index_size.append(t.rowCount())
        index.append(0)
    
    total = index_size[0]
    for t in index_size[1:]:
        total*=t
    index_len = len(index)
    i=0
    #passa por todos os valores possiveis e vê se devem ser deletados
    while i<total:
        if where_op.value(tables,index):
            set_op.value(tables,index)
        index[0]+=1
        for j in range(index_len):
            if index[j]>= index_size[j] and j+1< index_len:
                index[j]=0
                index[j+1]+=1
            else:
                break
        i+=1

#processos para a query de selection
def selectQuery(sep_query):
    #separa nas 4 partes da query
    select_q,from_q,where_q,order_q = separateSelectQuery(sep_query)
    #lida com o a clausula ON
    len_from= len(from_q)
    i = 0
    while i<len_from:
        if from_q[i] == ON:
            break
        i+=1
    if i+1<len_from:
        on_q =['('] + from_q[i+1:] + [')']
        if where_q != []:
            on_q += [AND]
        where_q = on_q+where_q
    if i<len_from:
        from_q = from_q[:i]
    #encontra as tabelas que farão parte, pelo parte do from
    tables = findTables(from_q)
    # pega as colunas da nova tabela
    columns = getColumns(select_q,tables)
    # descobre a operacao de where
    operation = createOperation(setupVariablesAndConstants(where_q,tables))
    
    id_order, id_asc = getOrder(order_q,columns,tables)
    return runSelect(columns,tables,operation,id_order,id_asc)

# processos para a query de insertion
def insertQuery(sep_query):
        insert_q,value_q = separateInsertQuery(sep_query)
        tables = findTables(insert_q)
        if len(tables) != 1:
            raise ValueError('Você apenas pode inserir um valor a uma table, não várias.')
        insertion = findValues(value_q)
        tables[0].add_instance(insertion)
        file = glob.glob("./"+insert_q[0]+".csv")
        df = pd.read_csv(file[0], index_col=None)
        texto=[]
        for i in range(len(insertion)):
            if not (type(insertion[i])==str):
                texto.append(insertion[i])
            else:
                texto.append("\'"+str(insertion[i].strip("\"\'"))+"\'")
        df.loc[len(df)] = texto
        df.to_csv(file[0], index=False)

#  processos para a query de deletion
def deleteQuery(sep_query):
        #separa nas 4 partes da query
        delete_q,from_q,where_q,order_q = separateSelectQuery(sep_query)
        #lida com o a clausula ON
        len_from= len(from_q)
        i = 0
        while i<len_from:
            if from_q[i] == ON:
                break
            i+=1
        if i+1<len_from:
            on_q =['('] + from_q[i+1:] + [')']
            if where_q != []:
                on_q += [AND]
            where_q = on_q+where_q
        if i<len_from:
            from_q = from_q[:i]
        #encontra as tabelas que farão parte, pelo parte do from
        tables = findTables(from_q)
        # pega a tabela que será deletada
        delete_tables = findTables(delete_q)
        len_tables = len(tables)
        if len(delete_tables) !=1:
            raise ValueError("Apenas pode-se deletar de uma table por vez.")
        t=0
        while t<len_tables:
            if tables[t].name == delete_tables[0].name:
                break
        if t == len_tables:
            raise ValueError("Apenas pode-se deletar de uma table que esteja na query.")

        # descobre a operacao de where
        operation = createOperation(setupVariablesAndConstants(where_q,tables))
        runDelete(t,tables,operation)
        dados = []
        for i in range(len(delete_tables[0].rows)):
            dados.append(delete_tables[0].rows[i])
        df = pd.DataFrame(dados)
        file = "./"+delete_tables[0].name+".csv"
        df.to_csv(file, index=False)

# processos para query de update
def updateQuery(sep_query):
        len_q =  len(sep_query)
        #muda de SET para FROM, para reutilizar funcao de select
        for i in range(len_q):
            if sep_query[i]==SET_TEXT:
                sep_query[i]=FROM
        update_q,set_q,where_q,order_q = separateSelectQuery(sep_query)
        tables = findTables(update_q)
        if(len(update_q)!=1):
            raise ValueError("Apenas pode-se atualizar uma tabela por vez.")
        set_operation = createOperation(setupVariablesAndConstants(set_q,tables),SET_OP)
        where_operation = createOperation(setupVariablesAndConstants(where_q,tables))
        runUpdate(tables,set_operation,where_operation)
        dados = []
        for i in range(len(tables[0].rows)):
            dados.append(tables[0].rows[i])
        df = pd.DataFrame(dados)
        file = "./"+tables[0].name+".csv"
        df.to_csv(file, index=False)

def importQuery(sep_query):
        len_q =  len(sep_query)
        if len_q == 3 and sep_query[1] == CSV:
            print(sep_query[2].strip("\'"))
            try:
                qntd = len(sep_query[2].strip("\'").split('/'))
                tamanho = len(sep_query[2].strip("\'").split('/')[qntd-1])
                nome = sep_query[2].strip("\'").split('/')[qntd-1][:tamanho-4]
                tabela = Table(sep_query[2].strip("\'").split('/')[qntd-1][:tamanho-4])
                print(sep_query[2].strip("\'").split('/'))
                df = pd.read_csv(sep_query[2].strip("\'"), index_col=None)
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
                existe = False
                for tables in database:
                    if(tables.name == nome):
                        existe = True
                if not existe:
                    database.append(tabela)
                    df.to_csv('./'+ nome + '.csv', index=False)
                else:
                    raise Exception("Tabela já existe.")
            except FileNotFoundError as e:
                raise Exception("Arquivo não existe.")
            print(df)
        elif len_q == 12 and sep_query[1] == MYSQL:
            try:
                mydb = mysql.connector.connect(
                    host=sep_query[3],
                    user=sep_query[5],
                    password=sep_query[7],
                    database= sep_query[9]
                )
                df = pd.read_sql_query("SELECT * FROM " + str(sep_query[11]), con=mydb)
                print(df)
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
            existe = False
            for tables in database:
                if(tables.name == str(sep_query[11])):
                    existe = True
            if not existe:
                df.to_csv('./'+ str(sep_query[11]) + '.csv', index=False, quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            else:
                raise Exception("Tabela já existe.")
            tabela = Table(str(sep_query[11]))
            df = pd.read_csv('./'+str(sep_query[11])+'.csv', index_col=None)
            print(df)
            for col in df.columns:
                tabela.add_column(col.strip(" '\""))
                print(col.strip(" '\""))
            print(tabela.columnNames)
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
            

# Analisa as queries de import e de select, delete, update e insert
def runQuery(query: str):
    sep_query = separator(query)
    if sep_query ==[]:
        return
    #faz o parsing adequado dependendo do tipo de query
    if SELECT == sep_query[0]:
        return selectQuery(sep_query)
    elif INSERT_INTO == sep_query[0]:
        insertQuery(sep_query)
    elif DELETE == sep_query[0]:
        deleteQuery(sep_query)
    elif UPDATE == sep_query[0]:
        updateQuery(sep_query)
    elif IMPORT == sep_query[0]:
        importQuery(sep_query)


            


        
        
        


        
        
    
