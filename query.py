from table import Table, TableCoordinate
from operation import Operation, createOperation
from separator import *
from syntax import *


        
#cria instancia com as colunas dadas
def createInstance(index,columns,tables):
    instance = []
    for column in columns:
        instance.append(tables[column.table_index].getValue(column.column,index[column.table_index]))
    return instance

# executa query de select
def run_select(columns,tables,operation:Operation,order):
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
    return new_table




def runQuery(query: str):
    sep_query = separator(query)
    if sep_query ==[]:
        return
    #se é uma query de select
    if SELECT == sep_query[0]:
        #separa nas 4 partes da query
        select_q,from_q,where_q,order_q = separateSelectQuery(sep_query)
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
        print(where_q)
        #encontra as tabelas que farão parte, pelo parte do from
        tables = findTables(from_q)
        # pega as colunas da nova tabela
        columns = getColumns(select_q,tables)
        # descobre a operacao de where
        operation = createOperation(setupVariablesAndConstants(where_q,tables))
        return run_select(columns,tables,operation,None)
        
        
        


        
        
    
