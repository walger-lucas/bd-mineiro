from separator import validParenthesis,removeUnecessaryParenthesis,separator,divisorWords
from table import TableCoordinate, Table
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
        return tables[self.table_coordinate.table_index].getValue(self.table_coordinate.column,indexes[self.table_coordinate.table_index])
    
    def __init__(self,table_coordinate: TableCoordinate):
        self.table_coordinate = table_coordinate

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
    
operationBias = (' e ',' ou ','==','!=','>','<','!') #tuple com o bias para separar operacoes, com as strings de cada operacao
def binaryOperationRecursion(operation,text,i):
        opA = text[:i]
        opB = text[i+1:]
        if opA == [] or opB == []:
            raise Exception("Operação '"+operation+"' necessita de duas entradas: "+ ' '.join(str(element) for element in text)+str(i))
        return opA,opB

def createOperation(sep_text):
    if sep_text == []:
        return ConstantOperation(True)
    
    if  not validParenthesis(sep_text):
        raise Exception("Parênteses não válidos: "+' '.join(str(element) for element in sep_text))
    removeUnecessaryParenthesis(sep_text)
    text_len = len(sep_text)
    in_parenthesis = 0
    next_operation= ''
    found_op = False
    for operation in operationBias:
        i = 0
        while i < text_len and not found_op:
            if sep_text[i]=='(':
                in_parenthesis+=1
            elif sep_text[i]==')':
                in_parenthesis-=1

            if in_parenthesis == 0 and operation == sep_text[i]:
                next_operation = operation
                found_op = True
                break
            
            i+=1
        if found_op:
            break

    if next_operation == operationBias[0]:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return AndOperation(createOperation(opA),createOperation(opB))
    elif next_operation == operationBias[1]:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return OrOperation(createOperation(opA),createOperation(opB))
    elif next_operation == operationBias[2]:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return EqualOperation(createOperation(opA),createOperation(opB))
    elif next_operation == operationBias[3]:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return NotEqualOperation(createOperation(opA),createOperation(opB))
    elif next_operation == operationBias[4]:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return GreaterThenOperation(createOperation(opA),createOperation(opB))
    elif next_operation == operationBias[5]:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return LesserThenOperation(createOperation(opA),createOperation(opB))
    elif next_operation == operationBias[6]:
        if sep_text[:i]!=[] or sep_text[i+1:]:
            raise Exception("Operação '" + next_operation+"' necessita de exatamente uma entrada: " + ' '.join(str(element) for element in sep_text))
        return NotOperation(createOperation(sep_text[i+1:]))
    elif next_operation == '':
        if len(sep_text) != 1:
            raise Exception("Operação deveria ser constante ou variável, potabrém não o é: "+ ' '.join(str(element) for element in sep_text))
        if type(sep_text[0]) == TableCoordinate:
            return VariableOperation(sep_text[0])
        return ConstantOperation(sep_text[0])
    return ConstantOperation(False)

            
            

