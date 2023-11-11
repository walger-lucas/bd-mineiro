from table import TableCoordinate
divisorWords = (' e ',' ou ','==','!=','<','>','!','(',')',',','própega','ladi','com','di cima', 'di baixo')
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
    separated_text = []
    txt_length = len(text)
    in_quotation = False
    qu_symbol = ''
    i=0
    word_start = 0
    while i <txt_length:
        # lida com quotations, nao lendo operacoes dentro de quotations
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
                    i+=len(dW)
                    word_start = i
                    break
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
        isNumber,isFloat = IsNumeric(word)
        if isNumber and isFloat:
            new_text.append(float(word)) 
            continue
        elif isNumber:
            new_text.append(int(word)) 
            continue
        #Procura por uma tabela.coluna no texto
        new_text.append(IsTable(word,tables))
    return new_text

# retorna se string eh um numero ou um inteiro ou nenhum
def IsNumeric(word):
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
def IsTable(word,tables):
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




