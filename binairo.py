import subprocess
from sys import exit
from itertools import combinations

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def celda(x, y):
    c = (x + 1) * n + (y + 1)
    return c

def fila(v):
    x = v/n
    return x - 1

def columna(v):
    y = v % n
    return y - 1

f = open ( 'input.txt' , 'r')
l = [[elem for elem in line] for line in f ]

# INEFICIENTE
s = []
for elem in l:
    try:
        elem.remove("\n")
        s.append(elem)
    except:
        s.append(elem)
#################

#tamaño fila ou columna do problema:
n = int(s[0][0])
s.remove(s[0])

#Imprimimos o problema inicial
for elem in s:
    print(elem)


#Numero variables:
nvars = n*n


#Numero de predicados
npreds = 0

text_file = open("Output.txt", "w")

for y in range(0, n):
    for x in range(0, n):
        var = celda(x, y)

        #Asignamos os valores booleanos as fichas xa colocadas
        if s[x][y] == '1':
            text_file.write("{0} 0\n".format(var))
            npreds+=1
        elif s[x][y] == '0':
            text_file.write("-{0} 0\n".format(var))
            npreds+=1

        #Regras do xogo
        else:
            """
            # Non pode haber 3 da mesma cor seguidas
            varY2 = celda(x, y + 1)
            varY3 = celda(x, y + 2)
            text_file.write("{0} {1} {2} 0\n".format(var, varY2, varY3))
            text_file.write("-{0} -{1} -{2} 0\n".format(var, varY2, varY3))
            npreds +=  2

            varX2 = celda(x + 1, y)
            varX3 = celda(x + 2, y)
            text_file.write("{0} {1} {2} 0\n".format(var, varX2, varX3))
            text_file.write("-{0} -{1} -{2} 0\n".format(var, varX2, varX3))
            npreds += 2
            """

            # Ten que haber as mesmas de cada cor en cada fila e columna
            laterais = []
            for i in range(0, n):
                laterais.append(celda(x + i, y))
                laterais.append(-celda(x+i,y))
            #Contamos o numero de positivos e negativos de cada combinacion
            for row in combinations(laterais, n):
                count = 0
                for elem in row:
                    # Se se encontra o mesmo elemento en signo oposto, saltamos esta iteracion
                    if -elem in row:
                        count = 1
                        break
                    if elem > 0:
                        count = count + 1
                    if elem < 0:
                        count = count - 1
                if count == 0:
                    regra = ""
                    for elem in row:
                        regra += str(elem) + " "
                    regra += "0\n"
                    text_file.write(regra)
                    npreds += 1

text_file.close()

# Engadimos ao comezo do ficheiro a liña inicial de SAT
line_prepender("Output.txt", "p cnf {0} {1}\n".format(nvars + 4*n, npreds))

# Chamada a Clasp
out = subprocess.Popen(['clasp', '--verbose=0', 'Output.txt'],
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT)

# Procesamos a saida do Clasp
claspOutput = out.communicate()
claspError = claspOutput[1]
claspPrint = str(claspOutput[0])
print(claspError)

claspPrint = claspPrint.split(" ")
claspPrint.pop()
claspPrint.pop()
try:
    del claspPrint[0]
except:
    print("UNSATISFIABLE\n")
    exit(0)



# Transforma de String a Int, quitando os caracteres de salto de liña
output = []
for elem in claspPrint:
    try:
        output.append(int(elem))
    except:
        output.append(int(elem[:-4]))

# Transforma a matriz de numeros a booleanos
outputList = []
for elem in output:
    if elem < 0:
        outputList.append(0)
    else:
        outputList.append(1)

# Imprimimos o resultado como se require
print("\n")
outputList = [str(elem) for elem in outputList]
for i in range(n,n*n + n, n):
    print(''.join(outputList[i:i+n]))

