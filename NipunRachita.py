# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:56:44 2018

@author: Nipun
"""

import sys
from ast import literal_eval
import operator
import collections
from collections import OrderedDict
from itertools import combinations





# function to implement MSApriori algorithm. It calls the other functions to succesfully execute and implement the MSApriori algorithm.
def MS_Apriori(T, MS, I, SDC, must_have, cannot_be_together):
    M = sort_itemset(I, MS)
    L, Icount = init_pass(MS, M, T)
    F1 = freq_1_itemset(L, MS, Icount, len(T), must_have)
    print_FreqSet(F1,1,Icount)
    freq_item_set_empty = False
    k = 1
    FreqSet = []
    while freq_item_set_empty == False:
        k = k + 1
        cCount = dict()
        cTailCount = dict()
        if (k == 2):
            C = level2_candidate_gen(L, SDC, MS, Icount, len(T))
            print(C)
        else:
            C = MScandidate_gen(FreqSet, SDC, MS, Icount, len(T))
        for c in C:
            c_child = string_convertor(c)
            cCount[c_child] = 0
            c_Tchild = c_child +'-'+string_convertor(c[1:])
            cTailCount[c_Tchild] = 0
        for t in T:
            tt = set(t)
            for c in C:
                c_child = string_convertor(c)
                c_Tchild = c_child + '-' + string_convertor(c[1:])
                cc = set(c)
                if cc.issubset(tt):
                    cCount[c_child] = cCount[c_child] + 1
                ccc = set(c[1:])
                if ccc.issubset(tt):
                    cTailCount[c_Tchild] = cTailCount[c_Tchild] + 1
        FreqSet = []
        PruneFreqSet = []
        for c in C:
            stringC = string_convertor(c)
            if (((cCount[stringC]/len(T))) >= MS[c[0]]):
                put_in_list = True
                must_have_in_list = False
                cset = set(c)
                FreqSet.append(c)
                for x in cannot_be_together:
                    xset = set(x)
                    if xset.issubset(cset):
                        put_in_list = False
                for y in must_have:
                    if y in c:
                        must_have_in_list = True
                if len(must_have) == 0:
                     must_have_in_list = True
                if put_in_list == True and must_have_in_list == True:
                    PruneFreqSet.append(c)
        if len(FreqSet) == 0:
            freq_item_set_empty = True 
        if freq_item_set_empty == False and (len(PruneFreqSet) >= 1):
            print_FreqSet(PruneFreqSet,k,cCount,cTailCount)





# function to convert input list tp string and return it.
def string_convertor(list_l):
    string_s = ','.join(map(str,list_l))
    return string_s




# function implementing initPass section of MSApriori algorithm.
def init_pass(MS, M, T):
    Icount = {}
    L = []
    for x in M:
        count = 0
        for i in range(0, len(T)):
            if x in T[i]:
                count = count + 1
        Icount[x] = count
    n = len(T)
    firstitem = False
    for x in M:
        if firstitem == False:
            if ((Icount[x] / n) >= MS[x]):
                L.append(x)
                l1 = x
                firstitem = True
        if firstitem == True:
            if ((Icount[x] / n) >= MS[l1]):
                if (l1 != x):
                    L.append(x)
    return L, Icount




# function to sort_itemset the itemset as in descending order.
def sort_itemset(I, MS):
    M = []
    MIS = sorted(MS.items(), key=operator.itemgetter(1))
#    print("MIS VALUES \n")
#    print(MIS)
    for i in range(0, len(MIS)):
        val1, val2 = MIS[i]
        M.append(val1)
    for i in range(0, len(M)):
        M[i] = (M[i])
    return M




# function to generate frequent itemset for k=1.
def freq_1_itemset(L, MS, Icount, n, must_have):
    F1 = []
    if (len(must_have) == 0):
        for x in L:
            if ((Icount[x] / n) >= MS[x]):
                view = []
                view.append(x)
                F1.append(view)
    else:
        for x in L:
            if ((Icount[x] / n) >= MS[x]) and (x in must_have):
                view = []
                view.append(x)
                F1.append(view)
    return F1




# function to generate candidate itemset for k=2. It takes F1 itemset in input.
def level2_candidate_gen(L, SDC, MS, Icount, n):
    C2 = []
    for l in L:
        if (Icount[l] / n) >= MS[l]:
            ind = L.index(l) + 1
            for h in L[ind:]:
                if (((Icount[h] / n) >= MS[l]) and (abs((Icount[h] / n) - (Icount[l] / n)) <= SDC)):
                    view = [l, h]
                    C2.append(view)
    return C2



# Function to implement candidate generation(k>2) section of MSApriori algorithm. It takes Fk-1 in input to generate Ck where k>2
def MScandidate_gen(F, SDC, MS, Icount, n):
    C = []
    for i in range(0,len(F)-1):
        for j in range(i+1,len(F)):
            f1 = F[i]
            f2 = F[j]
            if (f1[:(len(f1)-1)] == f2[:(len(f2)-1)] and MS[f2[len(f2)-1]] >= MS[f1[len(f1)-1]] and (abs((Icount[f1[len(f1)-1]]/n) - (Icount[f2[len(f2)-1]]/n)) <= SDC)):
                c = []
                for x in f1:
                    c.append(x)
                c.append(f2[-1])
                C.append(c)
                remove_item = False
                subset = [list(k) for k in combinations(c, len(c) - 1)]
                for s in subset:
                    slist = list(s)
                    if (c[0] in slist) or MS[c[1]] == MS[c[0]]:
                        if slist not in F:
                            remove_item =True
                if remove_item == True:
                    C.remove(c)
    return C



# function to write the frequent itemsets in outputfile.
def print_FreqSet(FreqSet,k,Icount,TailCount=0):
    fileF = open(outputfile, 'a+')
    if k == 1:
        fileF.write ("Frequent ")
        fileF.write (str(k))
        fileF.write ("-itemsets\n\n")
        for f in FreqSet:
            fileF.write ("\t")
            fileF.write (str(Icount[f[0]]))
            fileF.write (" : ")
            view = str(f)
            viewh = view.replace ("[","{")
            view = viewh.replace ("]","}")
            fileF.write (view)
            fileF.write ("\n")
        fileF.write ("\n\tTotal number of frequent ")
        fileF.write (str(k))
        fileF.write ("-itemsets = ")
        fileF.write (str(len(FreqSet)))
        fileF.write ("\n")
        fileF.write ("\n")
    else:
        fileF.write ("Frequent ")
        fileF.write (str(k))
        fileF.write ("-itemsets\n\n")
        for f in FreqSet:
            cCount = string_convertor (f)
            tCount = cCount +'-'+ string_convertor (f[1:])
            fileF.write ("\t")
            fileF.write (str(Icount[cCount]))
            fileF.write (" : ")
            view = str(f)
            viewh = view.replace ("[","{")
            view = viewh.replace ("]","}")
            fileF.write (view)
            fileF.write ("\n")
            fileF.write ("Tailcount = ")
            fileF.write (str(TailCount[tCount]))
            fileF.write ("\n")
        fileF.write ("\n\tTotal number of frequent ")
        fileF.write (str(k))
        fileF.write ("-itemsets = ")
        fileF.write (str(len(FreqSet)))
        fileF.write ("\n")
        fileF.write ("\n")
    fileF.close()




# Function to read tansactions and data pre-processing.
def GetTransactionData(filename):
    T = []
    with open(filename) as f:
        for line in f:                                  # reading transaction data from file line by line
            W = line.replace("<", "")                   # data pre-processing
            W = W.replace(">", "")
            W = W.replace("}{","},{")
            if W[0] != '{':
                W = '{'+W
            view = list(literal_eval (W))               # evaluating the input string to list
            if isinstance(view[0], set):
                for x in view:
                   cint = [int(i) for i in x]
                   T.append(cint)
            else:
                cint = [int(i) for i in view]
                T.append(cint)
    return T





# function to read parameters from parameter file
def GetParameters(filename='parameterfile.txt'):
    MS = {}
    I = []
    cannot_be_together = []
    must_have = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            if "MIS" in line:
                a, b = line.split("MIS(")
                a, b = b.split(") = ")
                MS[int(a)] = float(b)
                I.append(a)
            elif "SDC" in line:
                a, b = line.split("SDC = ")
                SDC = float(b)
            elif "cannot_be_together" in line:
                a, b = line.split("cannot_be_together: ")
                view = list(literal_eval (b))
#                print("View/dummy printing::: ")
#                print(view)
#                print(view[0])
                if isinstance(view[0], set):
                    for x in view:
                        cannot_be_together.append(list(x))
                else:
                    cannot_be_together.append(list(view))
            elif "must-have" in line:
                a, b = line.split("must-have:")
                must_have = [int(aa) for aa in b.split("or")]
    return MS, I, SDC, cannot_be_together, must_have



# output will be stored in file named "output-patterns.txt".
outputfile = 'output-patterns.txt'




# Main function to execute the program and call other functions
def main(inputdata, parameters):
    global outputfile
    print("*********WELCOME**********")
    print("MS-Apriori Implementation")
    print("Transaction Details")
    f = open(outputfile, 'w')
    T = GetTransactionData(inputdata)
    MS, I, SDC, cannot_be_together, must_have = GetParameters(parameters)
    MS_Apriori(T, MS, I, SDC, must_have, cannot_be_together)
    f.close


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])    # Argument 1 contains transaction data, argument 2 contains the parameter file. Takes command line arguments.