#!/usr/bin/python3
from re import *
import requests
import json
import sys
from getopt import getopt

# python3 down.py -i -l en/es          -> lista de ids que tem as linguas "en" e "es"
# python3 down.py                      -> IDs, descricoes e cods-Lingua das primeiras 20 talks
# python3 down.py -i -l en/es -t 40    -> lista de ids, com en/es, nas primeiras 40 etc
# python3 down.py             -t 40    -> IDs, descricoes e cods-Lingua das primeiras 40 talks
# se o -t nao for mult de 20 da exception
# python3 down.py  -i -l en/es -t 40 > ids.txt   para escrever para o ficheiro

ops, args = getopt(sys.argv[1:], "il:t:")
ops = dict(ops)
#print("Flags: ", ops, args)
if "-l" in ops:
    languages = split(r'/', ops.get("-l"))
    #print(languages[0] + " " + languages[1])

final = []
it = 1
lst = []

if "-t" in ops:
    Total = int(ops.get("-t"))
    if Total%20!=0:
        raise Exception("-t tem de ser múltiplo de 20.")
    numero = int(Total/20)   

    for x in range(it,numero+1):
        r = requests.get("https://ted2srt.org/api/talks?offset="+str(it*20))
        r.encoding = r.apparent_encoding
        lst.append(json.loads(r.text))
        it += 1
        

else:
    r = requests.get("https://ted2srt.org/api/talks?offset=20")
    r.encoding = r.apparent_encoding
    lst.append(json.loads(r.text))  

if "-i" not in ops:
    for texto in lst:
        for TED in texto:
            print("ID: " + str(TED["id"]))
            print(TED["description"])
            lan = TED["languages"]
            print("------------")
            for a in lan:
                print(a["languageCode"] + " " + a["languageName"])
            print("\n===\n")    
            final.append(TED)  
    print("Total de TEDs: "+str(final.__len__()))

else:
    for texto in lst:
        for TED in texto:
            lan = TED["languages"]
            i = 0
            cnt = languages.__len__()
            for a in lan:
                if a["languageCode"] in languages:
                    i += 1
                if i == cnt:
                    print(TED["id"])
                    break

