from table import Table

def merge(array:list,left:int,mid:int,right:int,id,asc=True):
    array_l = array[left:mid+1]
    array_r = array[mid+1:right+1]
    ind = left
    ind1 = 0
    ind2 = 0

    while ind1< -left+mid +1 and ind2< right-mid:
        if asc:
            if array_l[ind1][id] <= array_r[ind2][id]:
                array[ind] = array_l[ind1]
                ind1+=1
            else:
                array[ind] = array_r[ind2]
                ind2+=1
        else:
            if array_l[ind1][id] > array_r[ind2][id]:
                array[ind] = array_l[ind1]
                ind1+=1
            else:
                array[ind] = array_r[ind2]
                ind2+=1 
        ind+=1
    
    while ind1<-left+mid +1:
        array[ind] = array_l[ind1]
        ind1+=1
        ind+=1

    while ind2<right-mid:
        array[ind] = array_r[ind2]
        ind2+=1
        ind+=1

def mergeSort(array, begin:int,end:int,id,asc=True):
    if begin>=end:
        return
    mid: int = begin + int((end-begin)/2)
    mergeSort(array,begin,mid,id,asc)
    mergeSort(array,mid+1,end,id,asc)
    merge(array,begin,mid,end,id,asc)

# faz sorts da table, nos ids dados, ascendentes ou descendentes
def sortTable(table: Table,ids,asc):
    if ids == []:
        return
    table_len = table.rowCount()
    mergeSort(table.rows,0,table_len-1,ids[0],asc[0])
    
    ids_len = len(ids)
    i=0
    while i< ids_len-1:
        begin = 0
        j=0
        while j < table_len:
            if table.getValue(ids[i],j) != table.getValue(ids[i],begin):
                mergeSort(table.rows,begin,j-1,ids[i+1],asc[i+1])
                begin = j
            j+=1
        mergeSort(table.rows,begin,j-1,ids[i+1],asc[i+1])
        i+=1



