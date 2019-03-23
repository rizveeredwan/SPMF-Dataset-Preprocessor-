# python implementation to generate sequential pattern mining dataset from SPMF: Sequential Pattern Mining Section
import random

# file reading
fileName = raw_input("Give file name: ")
f = open(fileName, "r")
lines = f.readlines()
f.close()

max_value = 0
min_value = 1000000000000000000
# process
processedLines = []
for i in lines:
    temp = i.split('-2')  # removing the last string (-2)
    temp = temp[0].split('-1')  # segmenting by -1
    result = []
    for j in temp:
        save = j.split()  # removing the space
        if(len(save) >= 1):  # can not consider empty lists
            save[0] = int(save[0])
            max_value = max(max_value, save[0])
            min_value = min(min_value, save[0])
            result.append(save)  # each transaction is a segmented list
    # saving all the processed listed transictions
    processedLines.append(result)

print ("Total Lines: "+str(len(processedLines)))
print ("Existing Max value: "+str(max_value))
print ("Existing Min value: "+str(min_value))

numberOfDiscretizedSymbol = int(
    raw_input("Give Number of Discretized Symbol:(at least 1) "))

_range = (max_value - min_value+1)/(numberOfDiscretizedSymbol)


def returnDiscretizationSymbol(value):
    global _range
    global max_value
    global min_value
    global numberOfDiscretizedSymbol
    base = 97
    for i in range(1, numberOfDiscretizedSymbol+1):
        if(value < (min_value+i*_range)):
            sym = chr(base+(i-1))
            return sym
    return chr(base+numberOfDiscretizedSymbol-1)


# discretization section
discretizedTransactions = []
for i in processedLines:
    discretizedSequence = []
    for j in i:
        discretizedItemset = []
        for k in j:
            sym = returnDiscretizationSymbol(k)
            if(sym not in discretizedItemset):
                discretizedItemset.append(sym)
        sorted(discretizedItemset)  # sorted in same itemset
        discretizedSequence.append(discretizedItemset)
    discretizedTransactions.append(discretizedSequence)

# merging section
finalDiscretizedTransactions = []
for i in discretizedTransactions:
    takeList = i
    startIndex = 0
    while True:
        if((len(takeList) == 1) or (startIndex == len(takeList)-1)):
            break  # merging not possible
        r = random.randint(0, 1)
        if(r == 0):
            # no merging
            startIndex = startIndex+1
        else:
            # will merge
            for j in takeList[startIndex+1]:
                # next one
                if(j not in takeList[startIndex]):
                    takeList[startIndex].append(j)
            # sorting
            sorted(takeList[startIndex])
            del takeList[startIndex+1]
    finalDiscretizedTransactions.append(takeList)

f = open("spmf_dataset.txt", "w")
f.write(str(len(finalDiscretizedTransactions))+"\n")
for i in finalDiscretizedTransactions:
    res = ""
    for j in i:
        res = res+"{"
        for k in j:
            res = res+k
        res = res+"}"
    print res
    f.write(res+'\n')
f.close()
