from separator import validParenthesis,removeUnecessaryParenthesis
from table import TableCoordinate
from syntax import *
# Funções e classes que informam como sao realizadas operações de validação
class Operation:
    #virtual operation to be overwritten
    def value(self,tables,indexes):
        pass
    def print(self):
        pass
    def printAll(self):
        self.print()
        print()
class ConstantOperation(Operation):
    def value(self,tables,indexes):
        return self.constant

    def __init__(self,constant):
        self.constant = constant

    def print(self):
        print(str(self.constant),end='')

class VariableOperation(Operation):
    def value(self,tables,indexes):
        return tables[self.table_coordinate.table_index].getValue(self.table_coordinate.column,indexes[self.table_coordinate.table_index])
    
    def __init__(self,table_coordinate: TableCoordinate):
        self.table_coordinate = table_coordinate

    def print(self):
        print("Tabela"+str(self.table_coordinate.table_index)+".Coluna"+str(self.table_coordinate.column),end='')

class NotOperation(Operation):
    def __init__(self,op):
        self.op = op

    def value(self,tables,indexes):
        return not self.op.value(tables,indexes)
    
    def print(self):
        print(NOT+"(",end='')
        self.op.print()
        print(")",end='')

class NegativeOperation(Operation):
    def __init__(self,op):
        self.op = op

    def value(self,tables,indexes):
        return -self.op.value(tables,indexes)
    
    def print(self):
        print(SUBTRACT+"(",end='')
        self.op.print()
        print(")",end='')

class BinaryOperation(Operation):
        bin_symbol = ' '
        def value(self,tables,indexes):
            pass

        def __init__(self,opA,opB):
            self.opA = opA #operacao A, a esquerda
            self.opB = opB #operacao B, a direita
        
        def print(self):
            print("(",end='')
            self.opA.print()
            print(")"+self.bin_symbol+"(",end='')
            self.opB.print()
            print(")",end='')

class SetOperation(BinaryOperation):
    bin_symbol = SET
    def value(self,tables,indexes):
        t_id = self.opA.table_coordinate.table_index
        t_column = self.opA.table_coordinate.column
        tables[t_id].rows[indexes[t_id]][t_column] = self.opB.value(tables,indexes)

class SeparateOperation(BinaryOperation):
    bin_symbol = SEPARATE
    def value(self,tables,indexes):
        self.opA.value(tables,indexes)
        self.opB.value(tables,indexes)


class EqualOperation(BinaryOperation):
    bin_symbol = EQUAL
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) == self.opB.value(tables,indexes)

class NotEqualOperation(BinaryOperation):
    bin_symbol = NOT_EQUAL
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) != self.opB.value(tables,indexes)

class GreaterThenOperation(BinaryOperation):
    bin_symbol = GREATER
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) > self.opB.value(tables,indexes)

class LesserThenOperation(BinaryOperation):
    bin_symbol = LESSER
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) < self.opB.value(tables,indexes)
class MultiplyOperation(BinaryOperation):
    bin_symbol = MULTIPLY
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) * self.opB.value(tables,indexes)
class DivideOperation(BinaryOperation):
    bin_symbol = DIVIDE
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) / self.opB.value(tables,indexes)
class SumOperation(BinaryOperation):
    bin_symbol = SUM
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) + self.opB.value(tables,indexes)
class SubtractOperation(BinaryOperation):
    bin_symbol = SUBTRACT
    def value(self,tables,indexes):
        return self.opA.value(tables,indexes) + self.opB.value(tables,indexes)

class AndOperation(BinaryOperation):
    bin_symbol = AND
    def value(self,tables,indexes):
        if not self.opA.value(tables,indexes):
            return False
        elif (not self.opB.value(tables,indexes)):
            return False
        return True

class OrOperation(BinaryOperation):
    bin_symbol = OR
    def value(self,tables,indexes):
        if self.opA.value(tables,indexes):
            return True
        elif self.opB.value(tables,indexes):
            return True
        return False
    
operationBias = (SEPARATE,SET,AND,OR,EQUAL,NOT_EQUAL,GREATER,LESSER,NOT, MULTIPLY,DIVIDE,SUM,SUBTRACT) #tuple com o bias para separar operacoes, com as strings de cada operacao
def binaryOperationRecursion(operation,text,i):
        opA = text[:i]
        opB = text[i+1:]
        if opA == [] or opB == []:
            raise Exception("Operação '"+operation+"' necessita de duas entradas: "+ ' '.join(str(element) for element in text))
        return opA,opB

SET_OP = 0
VAL_OP = 1
GEN_OP = 3
def createOperation(sep_text,kind = GEN_OP):
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
    if kind == SET_OP and next_operation == SET:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return SetOperation(createOperation(opA,VAL_OP),createOperation(opB,GEN_OP))
    elif kind == SET_OP and next_operation==SEPARATE:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return SeparateOperation(createOperation(opA,SET_OP),createOperation(opB,SET_OP))
    elif kind == SET_OP:
        raise Exception("Operação de SET não válida.")
    
    if kind == VAL_OP and (len(sep_text) != 1 or type(sep_text[0]) != TableCoordinate):
        raise Exception("Operação de Variável não válida.")

    if next_operation == AND:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return AndOperation(createOperation(opA),createOperation(opB))
    elif next_operation == OR:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return OrOperation(createOperation(opA),createOperation(opB))
    elif next_operation == EQUAL:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return EqualOperation(createOperation(opA),createOperation(opB))
    elif next_operation == NOT_EQUAL:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return NotEqualOperation(createOperation(opA),createOperation(opB))
    elif next_operation == GREATER:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return GreaterThenOperation(createOperation(opA),createOperation(opB))
    elif next_operation == LESSER:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return LesserThenOperation(createOperation(opA),createOperation(opB))
    elif next_operation == DIVIDE:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return DivideOperation(createOperation(opA),createOperation(opB))
    elif next_operation == MULTIPLY:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return MultiplyOperation(createOperation(opA),createOperation(opB))
    elif next_operation == SUM:
        opA,opB = binaryOperationRecursion(next_operation,sep_text,i)
        return SumOperation(createOperation(opA),createOperation(opB))
    elif next_operation == SUBTRACT:
        if sep_text[:i]!=[] and sep_text[i+1:]==[] or sep_text[:i]==[] and sep_text[i+1:]==[]:
            raise Exception("Operação '" + next_operation+"' necessita de ao menos uma entrada: " + ' '.join(str(element) for element in sep_text))
        elif sep_text[:i]==[]:
            return NegativeOperation(createOperation(sep_text[i+1:]))
        return SubtractOperation(createOperation(sep_text[:i],sep_text[i+1:]))
        
    elif next_operation == NOT:
        if sep_text[:i]!=[] or sep_text[i+1:]==[]:
            raise Exception("Operação '" + next_operation+"' necessita de exatamente uma entrada: " + ' '.join(str(element) for element in sep_text))
        return NotOperation(createOperation(sep_text[i+1:]))
    elif next_operation == '':
        if len(sep_text) != 1:
            raise Exception("Operação deveria ser constante ou variável, potabrém não o é: "+ ' '.join(str(element) for element in sep_text))
        if type(sep_text[0]) == TableCoordinate:
            return VariableOperation(sep_text[0])
        return ConstantOperation(sep_text[0])
    raise Exception("Não foi possível analisar a operação " + next_operation + " neste contexto.")

            
            

