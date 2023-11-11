divisorWords = (' e ',' ou ','==','!=','<','>','!','(',')',',','própega','ladi','com','di cima', 'di baixo') 
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

def separator(text):
    separated_text = []
    txt_length = len(text)
    in_quotation = False
    qu_symbol = ''
    i=0
    word_start = 0
    while i <txt_length:
        if (text[i] == '"' or text[i] == "'") and (not in_quotation or qu_symbol==text[i]):
            in_quotation = not in_quotation
            qu_symbol = text[i]
        if not in_quotation:
            for dW in divisorWords:
                if i+len(dW)<=txt_length and text[i:i+len(dW)].lower() == dW:
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






