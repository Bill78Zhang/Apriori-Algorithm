from collections import Counter, defaultdict
import pandas as pd
import itertools

# method to get list without duplicates.
# function credit https://www.peterbe.com/plog/uniqifiers-benchmark
def f7(seq):
    narr = set()
    arrAdd = narr.add
    return [x for x in seq if not (x in narr or arrAdd(x))]

# method to change datasets into list of sets 
def changeSet(result_list):
    temp=[]
    for x in result_list.viewkeys():
        if type(x)==int:
            temp.append(set([x]))
        else:
            temp.append(set(itertools.chain(x)))
    return temp

# method to get frequently close itemsets
def frequent_close(yu,sh):
    for x in yu:
        vLen = len(x)
        for y in yu:
            wLen = len(y)
            if vLen+1==wLen:
                if x.issubset(y):
                    if vLen==1:
                        valk=next(iter(x))
                    else:
                        valk=tuple(x)
                    if sh.get(tuple(y)) == sh.get(valk):
                        sh.pop(valk)
                        break

# method to get frequently maxim itemsets
def frequent_maxim(yu, ava):
    for x in yu:
        vLen = len(x)
        for y in yu:
            wLen = len(y)
            if vLen+1==wLen:
                if x.issubset(y):
                    if vLen==1:
                        valk=next(iter(x))
                    else:
                        valk=tuple(x)
                    if ava.has_key(tuple(y)):
                        if ava.has_key(valk):
                            ava.pop(valk)
                        break

# get file name from the user
file_name = raw_input('Enter (.dat) File Name: ')

# reading data base files from the user
dataFrame = pd.read_csv(file_name,header=None)
dataList = dataFrame.values.tolist()
lenRows = len(dataList)

# method to get correct minimum support for all the dataset
while True:
    min_support = int(raw_input('Enter Minimum Support(%): '))
    if min_support <= 100 and min_support > 1:
        break
    else:
        print "enter valid minimum support value"
min_support = (lenRows * min_support)/100

data_list = []
for x in range(len(dataList)):
    arr_data = f7(dataList[x][0].split())
    data_list.append(map(int,arr_data))

data_counter = dict(Counter(itertools.chain.from_iterable(data_list)))
initial_counter = defaultdict(int,data_counter)

result_list = defaultdict(int)
k = 1
while True:   
    # method to generate list of values more than minimum support
    ans_list = []
    for key in initial_counter:
        if initial_counter.get(key) >= min_support:
            ans_list.append(key)
            result_list.update({key:initial_counter.get(key)})
    k += 1
    if k>=3:
        ans_list = list(Counter(itertools.chain.from_iterable(ans_list)))
    
    # method to generate combinations of values from initial_counter    
    combine_values = list(itertools.combinations(ans_list,k))
    
    # this loop get the system exit whenever there are no iterations
    if not combine_values:
        print("Exit")
        print("Frequent Itemsets: ")
        print result_list.keys()
        yu = changeSet(result_list)
        sh=result_list.copy()
        frequent_close(yu,sh)
        print("Frequent Close Itemsets: ")
        print sh.keys()
        ava = result_list.copy()
        frequent_maxim(yu,ava)
        print("Frequent Maximum Itemsets: ")
        print ava.keys()
        raise SystemExit
    
    # this loop gets counter combinations for the values    
    initial_counter = defaultdict(int)    
    for x in combine_values:
        x1=set(x)
        for y in data_list:
            y1=set(y)
            if x1.issubset(y1):
                initial_counter[x] += 1