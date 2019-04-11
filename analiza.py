from pyMorfologik import Morfologik
from pyMorfologik.parsing import ListParser
from nltk.util import ngrams
import nltk, tkinter, sys, random, pyodbc, re
#from pydic import PyDic
#dic = PyDic('sjp.pydic')


server='KOMPUTER\SQLEXPRESS'
database='analizaDanych'
user = 'Jan'
password=''
connection_string = "Driver={SQL Server Native Client 11.0};""Server=KOMPUTER\SQLEXPRESS;""Database=analizaDanych;""Trusted_Connection=yes;"
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

command = "select top 1 * from synonimy"
cursor.execute(command)
for row in cursor:
    print(f'row={row}')
print()

#wczytany tekst
tekst = "samoistny Text mining (eksploracja tekstu) ogólna nazwa metod eksploracji danych służących do wydobywania danych z tekstu i ich późniejszej obróbki. Eksploracyjna analiza tekstów (text mining) jest stosunkowo młodą multidyscyplinarną dziedziną.".lower()
tokeny = nltk.word_tokenize(tekst)
print(tokeny)

# usunięcie stop_listy
lines=[]
lines= open('stopLista.txt').read()
filtr=[]
j=0
#filtr = [w for w in tokeny if not w in lines]
for w in tokeny:
    if not w in lines:
        if not re.match('(.*)[,.:;!?%](.*)', w):
            filtr.append(w)


# lemmantyzacja
parser = ListParser()
stemmer = Morfologik()
out = stemmer.stem(filtr,parser)
print('out')
#out1= str(out)
#print(out)

#zapis sparsowanych słów do tablicy
insert_slowo ="insert into slowo (slowo, synonim, cz_zdania )values(?,?,?)"

#for w2 in tokeny:
slowo = stemmer.stem(filtr, parser)
#for w1 in slowo:
#    list.append(w1)
for o in out:
    #print(o)
    o1=str(o).split(")")
    #print(o1)
    o2 = str(o1).replace('["(','')
    o2 = o2.replace('{','')
    o2 = o2.replace("':","'" )
    o2 = o2.replace("[",",")
    o2 = o2.replace(']}','')
    o2 = o2.replace('",', '')
    o2 = o2.replace("'']", '')
    o2 = o2.replace(", }", '')
    o3 = o2[0:o2.find(',')]
    o3 = o3.replace("'",'')
    o4 = o2[o2.find("',"):o2.find(",'")]
    o4 = o4.replace("'",'')
    o4 = o4.replace(",", '')
    o5 = o2[o2.find(",'"):o2.__len__()]
    o5 = o5.replace("'",'')
    o5 = o5.replace(",", '')
    #print(o3)
    #print(o4)
    #print(o5)
    #cursor.execute(insert_slowo,(o3,o4,o5))
    #connection.commit()
print('po slowie')


command = "select synonimy from synonimy where slowo=?"
print("\nSynonimy:")
for w1 in filtr:
    cursor.execute(command, w1)
    for row in cursor:
        print(f'row={row}')
print("Po Synonimach")


print("\nBigramy:")
print(list(ngrams(filtr, 2)))
print("Po bigramach")
