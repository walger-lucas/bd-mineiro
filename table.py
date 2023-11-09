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
        self.name = name.lower()
        self.columnNames = [] #array with names for each column
        self.rows = [] #Array with an array for each instance
    
    # adiciona uma instancia nas colunas
    def add_instance(self,instance):
        inst_size = len(instance)
        common_size=len(self.columnNames)
        for i in range(common_size-inst_size):
            instance.append(None)
        self.rows.append(instance)
    
    # adiciona uma coluna
    def add_column(self,name):
        self.columnNames.append(name.lower())
        for row in self.rows:
            row.append(None);
    
    def print(self):
        format_table = "{:>15}"* len(self.columnNames)
        print(format_table.format(*self.columnNames))
        print('-'*len(self.columnNames)*15)
        for row in self.rows:
            print(format_table.format(*printable_none(row)))
            


    #if has column returns position of it, if nonexistent returns -1 test
    def getColumn(self,name):
        try:
            pos = self.columnNames.index(name.lower())
            return pos
        except ValueError:
            return -1


