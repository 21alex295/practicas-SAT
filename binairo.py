import subprocess
from sys import exit
from itertools import combinations, permutations
from math import floor, ceil


# Facer lista de nxn coas reglas, para obter as filas e as columnas das regras
# Logo, con esto facemos as permutacions de 4 para a segunda regra
def filasColumnas(lista):
    """
    :param lista: Lista de formato nxn coas regras do problema
    :return: as filas e columnas da lista
    """
    totalVerticais = []
    for i in range(0, n):
        totalVerticais.append([row[i] for row in lista])
    return totalVerticais, lista


def list_to_nxn(lista):
    """
    Convirte a lista de regras nunha lista nxn
    :param lista: lista de regras do problema
    :return: lista das regras no formato nxn
    """
    result = []
    for i in range(0, n ):
        row = []
        for j in range(0, n ):
            row.append(lista[celda(i, j)] + 1)
        result.append(row)
    return result

def empty_list():
    """
    :return: Lista vacia en formato nxn
    """
    result = []
    for i in range(0, n):
        row = []
        for j in range(0, n):
            row.append(0)
        result.append(row)
    return result


def line_prepender(filename, line):
    """
    Engade liña ao comezo do ficheiro co numero de regras e predicados
    :param filename: Ficheiro no que escribir
    :param line: Liña co numero de regras e predicados
    """
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def celda(i, j):
    c = i * n + j
    return c


def fila(v):
    i = floor(v/n)
    return i


def columna(v):
    j = (v) % n
    return j

# Abrimos o ficheiro de entrada en modo lectura
f = open ('input.txt' , 'r')

# Gardamos nunha lista de listas os valores do input
l = [[elem for elem in line] for line in f]

# Quitamos da lista os saltos de liña. E INEFICIENTE porque facemos unha copia
# da lista
s = []
for elem in l:
    try:
        elem.remove("\n")
        s.append(elem)
    except:
        s.append(elem)
#################

# Tamaño fila ou columna do problema. Primeiro xuntamos os numeros da primeira
# lista (numero de filas/columnas) nun string e logo pasamolo a int
tFila = ''.join(s[0])
n = int(tFila)

# Eliminamos o numero fila/columna porque non o necesitaremos mais
s.remove(s[0])

# Imprimimos o problema inicial
for elem in s:
    print(*elem)

# Numero variables:
nvars = n*n

# Numero de predicados
npreds = 0

# Abrimos o ficheiro de saida
text_file = open("Output.txt", "w")

# Asignamos os valores booleanos as fichas que xa estan colocadas e
# gardamos as posibles regras (celdas) nunha lista
rulesList = []
for i in range(0, n):
    for j in range(0, n):
        var = celda(i, j)
        rulesList.append(var)
        if s[i][j] == '1':
            text_file.write("{0} 0\n".format(var + 1))
            npreds += 1
        elif s[i][j] == '0':
            text_file.write("-{0} 0\n".format(var + 1))
            npreds += 1


# Pasamos a lista de regras a unha lista de listas nxn
rulesList_nxn = list_to_nxn(rulesList)


##############################################################################
########################## Regras do xogo ####################################
##############################################################################

# REGRA No 1 => Non pode haber 3 da mesma cor seguidas
#  ¬(p ^ q ^ r)
#     ==
#  ¬p ∨ ¬q ∨ ¬r
for i in range(0, n):
    for j in range(0, n):
        var = celda(i, j)
        # Comprobamos os dous veciños da fila pola dereita
        if j + 2 < n:
            varY2 = celda(i, j + 1)
            varY3 = celda(i, j + 2)
            text_file.write("{0} {1} {2} 0\n".format(
                var + 1, varY2 + 1, varY3 + 1))
            text_file.write("-{0} -{1} -{2} 0\n".format(
                var + 1, varY2 + 1, varY3 + 1))
            npreds +=  2
        # Comprobamos os dous veciños da columna por abaixo
        if i + 2 < n:
            varX2 = celda(i + 1, j)
            varX3 = celda(i + 2, j)
            text_file.write("{0} {1} {2} 0\n".format(
                var + 1, varX2 + 1, varX3 + 1))
            text_file.write("-{0} -{1} -{2} 0\n".format(
                var + 1, varX2 + 1, varX3 + 1))
            npreds += 2


# REGRA 2 => Ten que haber as mesmas de cada cor en cada fila e columna
# p ^ q ^ r --> ¬s
#        ==
# ¬p ∨ ¬q ∨ ¬r ∨ ¬sº


# Obtemos as filas e columnas da lista de regras
verticais, laterais = filasColumnas(rulesList_nxn)

# En cada fila facemos as combinacions de (n/2 + 1) elementos
for lat in laterais:
    for row in combinations(lat, int(n/2 + 1)):
        regraBlancas = ""
        regraNegras = ""
        for item in row:
            regraBlancas += str(item) + " "
            regraNegras+= "-"+ str(item) + " "
        regraBlancas += "0\n"
        regraNegras += "0\n"
        text_file.write(regraBlancas)
        text_file.write(regraNegras)
        npreds += 2
for ver in verticais:
    for column in combinations(ver, int(n/2 + 1)):
        regraBlancas = ""
        regraNegras = ""
        for item2 in column:
            regraBlancas += str(item2) + " "
            regraNegras+= "-"+ str(item2) + " "
        regraBlancas += "0\n"
        regraNegras += "0\n"
        text_file.write(regraBlancas)
        text_file.write(regraNegras)
        npreds += 2


# REGRA 3 => Non pode haber filas/columnas repetidas
for fila1 in laterais:
    for fila2 in laterais:
        listaPs = []
        regraP = ""
        if fila1 != fila2:
            if fila1 != fila2:
                for i in range(0, len(fila1)):
                    nvars += 1
                    text_file.write("-{0} {1} {2} 0\n".format(nvars, fila1[i], fila2[i]))
                    text_file.write("-{0} -{1} -{2} 0\n".format(nvars, fila1[i], fila2[i]))
                    text_file.write("-{0} {1} {2} 0\n".format(fila1[i], fila2[i], nvars))
                    text_file.write("{0} -{1} {2} 0\n".format(fila1[i], fila2[i], nvars))
                    npreds += 4
                    listaPs.append(nvars)
                for elem in listaPs:
                    regraP += str(elem) + " "
                regraP += " 0\n"
                text_file.write(regraP)
                npreds += 1


for col1 in verticais:
    for col2 in verticais:
        listaPs = []
        regraP = ""
        if col1 != col2:
            for i in range(0, len(col1)):
                nvars += 1
                text_file.write("-{0} {1} {2} 0\n".format(nvars, col1[i], col2[i]))
                text_file.write("-{0} -{1} -{2} 0\n".format(nvars, col1[i], col2[i]))
                text_file.write("-{0} {1} {2} 0\n".format(col1[i], col2[i], nvars))
                text_file.write("{0} -{1} {2} 0\n".format(col1[i], col2[i], nvars))
                npreds += 4
                listaPs.append(nvars)
            for elem in listaPs:
                regraP += str(elem) + " "
            regraP += " 0\n"
            text_file.write(regraP)
            npreds += 1


######################################################################
######################################################################
######################################################################

text_file.close()

# Engadimos ao comezo do ficheiro a liña inicial de SAT
line_prepender("Output.txt", "p cnf {0} {1}\n".format(nvars, npreds))

# Chamada a Clasp
out = subprocess.Popen(['clasp', '--verbose=0', 'Output.txt'],
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT)

# Procesamos a saida do Clasp
claspOutput = out.communicate()
claspError = claspOutput[1]
claspPrint = str(claspOutput[0])
claspPrint = claspPrint.split(" ")

# Elimina caracteres indesexados da saida
claspPrint.pop()
claspPrint.pop()
try:
    del claspPrint[0]
except:
    print("UNSATISFIABLE\n")
    exit(0)



# Transforma a saida de clasp de String a matriz de numeros
output = []
for elem in claspPrint:
    try:
        output.append(int(elem))
    except:
        # Se hai un salto de liña, eliminase aqui
        try:
            output.append(int(elem[:-3]))
        except:
            # Imprime o erro nun caso inesperado
            print(claspOutput[0])



print("\n")

# Convirte o resultado de clasp na matriz de 1's e 0's
visitados = []
result = empty_list()
for pos in output:
        if abs(pos) <= n*n:
            num = rulesList[abs(pos) - 1]
            x = fila(num)
            y = columna(num)
            if (x, y) not in visitados:
                visitados.append((x, y))
                visitados.append((x, y))
                if pos > 0:
                    result[x][y] = 1
                elif pos < 0:
                    result[x][y] = 0

for elem in result:
    print(*elem, sep="")
# Imprimime a matriz tal e como se pide
with open('result.txt', 'w') as f:
    for elem in result:
        print(*elem, sep="", file=f)