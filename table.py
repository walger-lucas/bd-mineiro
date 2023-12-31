import pandas as pd

##Transforma o row, tirando seus nones e trocando por uma string 'Null'
def printable_none(row):
    new_row = []
    for r in row:
        if r == None:
            new_row.append('Null')
        else:
            new_row.append(r)
    return new_row

class Table:

    def __init__(self,name):
        self.name = name
        self.columnNames = [] #array with names for each column
        self.rows = [] #Array with an array for each instance
    
    # adiciona uma instancia nas colunas
    def add_instance(self,instance):
        inst_size = len(instance)
        common_size=len(self.columnNames)
        for i in range(common_size-inst_size):
            instance.append(None)
        if inst_size>common_size:
            self.rows.append(instance[0:common_size])
        else:
            self.rows.append(instance)
    
    # adiciona uma coluna
    def add_column(self,name):
        self.columnNames.append(name)
        for row in self.rows:
            row.append(None)
    
    def print(self):
        max = 0
        for name in self.columnNames:
            size = len(name)
            if max< size:
                max = size
        for row in self.rows:
            for instance in row:
                size = len(str(instance))
                if max< size:
                    max = size

        format_table = ("{:>"+str(max+4)+"}")* len(self.columnNames)
        print(format_table.format(*self.columnNames))
        print('-'*len(self.columnNames)*(max+4))
        for row in self.rows:
            print(format_table.format(*printable_none(row)))

    #se possui coluna a encontra, dependente de case
    def getColumn(self,name):
        try:
            pos = self.columnNames.index(name)
            return pos
        except ValueError:
            return -1
        
    def getValue(self,column,index):
        return self.rows[index][column]
    
    def rowCount(self):
        return len(self.rows)
    
    #guarda tabela em csv
    def store(self):
        dados = []

        headers =[]
        for header in self.columnNames:
           headers.append( "\'"+header+"\'" )
        dados.append(headers)
        row_len = self.rowCount()
        column_len = len(self.columnNames)
        for i in range(row_len):
            row = []
            for dado in self.rows[i]:
                if type(dado) == str:
                   dado = "\'"+dado+"\'"
                row.append(dado)
            dados.append(row)
        df = pd.DataFrame(dados)
        file = "./"+self.name+".csv"
        df.to_csv(file, index=False,header=False)

    
    
class TableCoordinate:
   def __init__(self,table_index,column):
       self.table_index = table_index
       self.column = column
    


