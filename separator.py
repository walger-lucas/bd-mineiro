from table import TableCoordinate
from syntax import *
from database import database
# Funcoes que fazem parte do parsing de strings, e 
# transformar este parsing em objetos úteis para a realização das queries

# palavras de divisao da string de parsing
divisorWords = (AND,OR,EQUAL,NOT_EQUAL,LESSER,GREATER,NOT,'(',')',',',SELECT,FROM,WHERE,ASC, DESC,ON, JOIN)
# append da palavra nao divisora entre palavras divisoras
def tryAppendLastWord(text,word_start,word_end, separated_text):
    if word_start >= len(text):
        return
    j=0
    while  j< word_end-word_start and text[word_start+j] == " ":
        j+=1
    start = word_start+j
    if start != word_end:
        j=0
        while word_end+j> word_start and text[word_end-1+j] == " " :
            j-=1
        separated_text.append(text[start:word_end+j])

#divide texto em uma lista de variáveis e operacoes
def separator(text):
    text = " "+text+" "
    separated_text = []
    txt_length = len(text)
    in_quotation = False
    qu_symbol = ''
    i=0
    word_start = 0
    while i <txt_length:
        # lida com quotations, nao lendo operacoes dentro de quotations
        found_dw = False
        if (text[i] == '"' or text[i] == "'") and (not in_quotation or qu_symbol==text[i]):
            in_quotation = not in_quotation
            qu_symbol = text[i]
        if not in_quotation:
            #tenta encontrar palavras divisoras na substring
            for dW in divisorWords:
                if i+len(dW)<=txt_length and text[i:i+len(dW)].lower() == dW:
                    #se encontrou uma, primeiro adicione a palavra nao divisora anterior a palavra divisora
                    tryAppendLastWord(text,word_start,i,separated_text)
                    separated_text.append(dW)
                    found_dw=True
                    i+=len(dW)
                    word_start = i
                    break
        if not found_dw:
            i+=1
    tryAppendLastWord(text,word_start,i,separated_text)
    return separated_text

#testa se os parentesis sao validos
def validParenthesis(sep_text):
    num_parenthesis = 0
    for word in sep_text:
        if word == '(':
                num_parenthesis+=1
        elif word == ')':
                num_parenthesis-=1
        if num_parenthesis < 0:
             return False
    if num_parenthesis == 0:
         return True
    return False


# remove os parentesis externos de um texto separado por palavra divisora se esses parentesis nao forem necessarios para a validade do texto
def removeUnecessaryParenthesis(sep_text):
    if len(sep_text)==0:
         return
    while sep_text[0]== '(' and sep_text[-1]==')' and validParenthesis(sep_text[1:-1]):
         sep_text.pop()
         sep_text.pop(0)

#faz setup de variaveis e constantes, apenas para statements where
def setupVariablesAndConstants(sep_text, tables):
    new_text = [] #variável que guardará nova forma do texto
    for word in sep_text:
        #passa palavras divisoras sem analisar
        if word in divisorWords:
            new_text.append(word)
            continue
        # encontra quotations e os tira, tornando apenas uma string comum
        if (word[0]== '"' and word[-1]== '"') or (word[0]== "'" and word[-1]== "'"):
            new_text.append(word[1:-1])
            continue
        #analisa se apenas há numeros e ou um ponto, e os transforma em ints e floats
        isNumber,isFloat = isNumeric(word)
        if isNumber and isFloat:
            new_text.append(float(word)) 
            continue
        elif isNumber:
            new_text.append(int(word)) 
            continue
        #Procura por uma tabela.coluna no texto
        new_text.append(isTable(word,tables))
    return new_text

# retorna se string eh um numero ou um inteiro ou nenhum
def isNumeric(word):
    isFloat = False
    isNumber = True
    for c in word:
        if c=='.' and isFloat==False:
            isFloat=True
        elif c=='.':
            isNumber=False
            break
        elif c<'0' or c>'9':
            isNumber=False
            break
    return isNumber,isFloat

# testa se palavra eh uma coluna de alguma das tabelas dads, e retorna um TableCoordinate caso sim, e uma Exception caso nao
def isTable(word,tables):
    len_word = len(word)
    dot_position = -1
    for i in range(len_word):
        if (word[i]=='.' and dot_position == -1 ):
            dot_position=i
        elif word[i]=='.':
            raise Exception(word + "não é uma variável válida.")
    if dot_position == -1:
        raise Exception(word + "não é uma variável válida.")
    tables_len = len(tables)
    found_table = False
    for j in range(tables_len):
        if tables[j].name == word[:dot_position]:
            column_id = tables[j].getColumn(word[dot_position+1:])
            found_table=True
            if column_id!=-1:
                return TableCoordinate(j,column_id)
            else:
                raise Exception("Tabela " + tables[j].name + " não possui coluna " + word[dot_position+1:]+" .")
            break
    if not found_table:
        raise Exception("Não há uma tabela " + word[:dot_position]+ " nesta query.")


#separa todas as funcoes do select
def separateSelectQuery(sep_query):
    pos_from = -1
    pos_where = -1
    pos_order = -1
    query_len = len(sep_query)
    for i in range(query_len):
        if sep_query[i]== FROM and pos_from==-1:
            pos_from = i
        elif sep_query[i]== WHERE and pos_where==-1:
            pos_where = i
        elif sep_query[i]== ORDER_BY and pos_order==-1:
            pos_order = i
        elif sep_query[i]== FROM and pos_from!=-1:
            raise Exception(FROM+" apenas pode aparecer uma vez na query.")
        elif sep_query[i]== WHERE and pos_where!=-1:
            raise Exception(WHERE+" apenas pode aparecer uma vez na query.")
        elif sep_query[i]== ORDER_BY and pos_order!=-1:
            raise Exception(ORDER_BY+" apenas pode aparecer uma vez na query.")
        elif sep_query[i]== SELECT and i >0:
            raise Exception(ORDER_BY+" deve aparecer  apenas no inicio")
    if pos_where < pos_from and pos_where !=-1:
        raise Exception(WHERE + "deve aparecer depois de"+ FROM)
    if pos_where > pos_order and pos_order!=-1:
        raise Exception(ORDER_BY + "deve aparecer depois de"+ WHERE)
    where_text =sep_query[pos_where+1:]
    order_text =sep_query[pos_order+1:]
    from_text = sep_query[pos_from+1:]
    select_text = sep_query[1:pos_from]
    if pos_order == -1:
        order_text=[]
    else:
        where_text= sep_query[pos_where+1:pos_order]
    if pos_where == -1:
        where_text = []
    else:
        from_text = sep_query[pos_from+1:pos_where]
    if pos_from == -1:
        raise Exception("É obrigatório a operação " +FROM + " na query")
    return select_text,from_text,where_text,order_text

# encontra as colunas das tables que devem ser adicionadas
def getColumns(select_q,tables):
    columns = []
    if select_q !=[] and select_q[0] == '*':
        table_len = len(tables)
        for i in range(table_len):
            column_len = len(tables[i].columnNames)
            for j in range(column_len):
                columns.append(TableCoordinate(i,j))
        return columns

    for word in select_q:
        if word == ',':
            continue
        columns.append(isTable(word,tables))
    return columns

# encontra as tabelas da database que serão utilizadas
def findTables(from_q):
    tables = []
    for word in from_q:
        if word == ',' or word == JOIN:
            continue
        table_found = False
        for table in database:
            if table.name == word:
                tables.append(table)
                table_found=True
                break
        if not table_found:
            raise Exception("Não há uma tabela " + word+ " nesta query.")
    return tables