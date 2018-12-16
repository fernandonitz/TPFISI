from random import randint
import os.path

DIVISION_PERCENTAGE = 5
RUTA = os.getcwd()

arch = open(RUTA + "\\data_handling.csv",'r')
testSet = open(RUTA + "\\testSet.csv",'w')
trainSet = open(RUTA + "\\trainSet.csv",'w')

lineas = arch.readlines()
count = len(lineas)

cantLinesToCut = int(count / 100 * DIVISION_PERCENTAGE)
nRandoms = []

for i in range(cantLinesToCut):
    n = randint(0, count-1)
    nRandoms.append(n)

i = 0
j = 0

for line in lineas:
    if i in nRandoms:
        testSet.write(line)
    else:
        trainSet.write(line)
    i = i + 1
    if (j == 50000):
        print ("leyendo la linea n°" + str(i))
        j = 0
    j = j + 1

arch.close()
testSet.close()
trainSet.close()
