class Operation:
    #virtual operation to be overwritten
    def value(self,tables,indexes):
        pass

class ConstantOperation(Operation):
    def value(self,tables,indexes):
        return self.constant

    def __init__(self,constant):
        self.constant = constant

class VariableOperation(Operation):
    def value(self,tables,indexes):
        return tables[self.table][indexes[self.table]][self.column]

    def __init__(self,i,j):
        self.table = i #qual tabela
        self.column = j #qual coluna

class NotOperation(Operation):
    def __init__(self,op):
        self.op = op

    def value(self,tables,indexes):
        return not self.op.value(tables,indexes)

class BinaryOperation(Operation):
        def value(self,tables,indexes):
            pass

        def __init__(self,opA,opB):
            self.opA = opA #operacao A, a esquerda
            self.opB = opB #operacao B, a direita

class EqualOperation(BinaryOperation):
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) == self.opB.value(tables,indexes)

class NotEqualOperation(BinaryOperation):
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) != self.opB.value(tables,indexes)

class GreaterThenOperation(BinaryOperation):
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) > self.opB.value(tables,indexes)

class LesserThenOperation(BinaryOperation):
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) < self.opB.value(tables,indexes)

class AndOperation(BinaryOperation):
    def value(self,tables,indexes):
        if not self.opA.value(tables,indexes):
            return False
        elif (not self.opB.value(tables,indexes)):
            return False
        return True

class OrOperation(BinaryOperation):
    def value(self,tables,indexes):
        if self.opA.value(tables,indexes):
            return True
        elif self.opB.value(tables,indexes):
            return True
        return False
    
operationBias = (' e ',' ou ','==','!=','<','>','!') #tuple com o bias para separar operacoes, com as strings de cada operacao