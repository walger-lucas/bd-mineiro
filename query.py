from table import Table, TableCoordinate
from operation import Operation, createOperation
from separator import *
from syntax import *


        
class SelectQuery:
    def __init__(self,columns,tables,operation:Operation,order):
        self.columns : list[TableCoordinate] = columns
        self.tables : list[Table] = tables
        self.operation : Operation = operation
        self.order = order

    def run(self):

        new_table = Table("table")
        #adiciona as novas colunas em ordem a tabela
        for column in self.columns:
            new_table.add_column(self.tables[column.table_index].name+"_"+self.tables[column.table_index].columnNames[column.column])


        if self.tables == []:
            return None
        #inicializa indexes
        index = []
        index_size = []
        for t in self.tables:
            index_size.append(t.rowCount())
            index.append(0)
        
        total = index_size[0]
        for t in index_size[1:]:
            total*=t
        index_len = len(index)
        i=0
        
        #passa por todos os valores possiveis
        while i<total:
            if self.operation.value(self.tables,index):
                new_table.add_instance(self.create_instance(index))
            index[0]+=1
            for j in range(index_len):
                if index[j]>= index_size[j] and j+1< index_len:
                    index[j]=0
                    index[j+1]+=1
                else:
                    break
            i+=1
        return new_table

    def create_instance(self,index):
        instance = []
        for column in self.columns:
            instance.append(self.tables[column.table_index].getValue(column.column,index[column.table_index]))
        return instance


def runQuery(query: str):
    sep_query = separator(query)
    if sep_query ==[]:
        return
    #se é uma query de select
    if SELECT == sep_query[0]:
        #separa nas 4 partes da query
        select_q,from_q,where_q,order_q = separateSelectQuery(sep_query)

        #encontra as tabelas que farão parte, pelo parte do from
        tables = findTables(from_q)
        # pega as colunas da nova tabela
        columns = getColumns(select_q,tables)
        # descobre a operacao de where
        operation = createOperation(setupVariablesAndConstants(where_q,tables))
        select_query = SelectQuery(columns,tables,operation,None)
        return select_query.run()
        
        


        
        
    
