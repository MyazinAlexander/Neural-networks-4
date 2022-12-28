import xml.etree.ElementTree as xml
import os
import sys
from sys import argv
import math

def evaluate(matrix, vector):
    new_matrix = []

    for layer in matrix:
        tempStr = []
        for x in layer:
            for neuron in x:
                value = 0
                for i in range(len(vector)):
                    value += neuron[i] * vector[i]
                value = value / (1 + abs(value))
                tempStr.append(value)
            new_matrix.append(tempStr)
            vector = tempStr
    return new_matrix


if (len(argv) == 1):
    print('Не было передано аргументов!')
    exit()

source1Path = argv[1][7::]
source2Path = argv[2][7::]
destination1Path = argv[3][8::]
destination2Path = argv[4][8::]

if (not os.path.isfile(source1Path)):
    print(f"Не удалось открыть файл-источник ({source1Path}), такого файла нет!")
    exit()

if (not os.path.isfile(source2Path)):
    print(f"Не удалось открыть файл-источник ({source2Path}), такого файла нет!")
    exit()

# считаем вектор и матрицу

vector = [int(x) for x in open(source2Path).read().split()]
vectorLength = len(vector)

matrix = []
inputFile = open(source1Path).readlines()

index = 0
for line in inputFile:
    matrixRow = []
    index += 1
    neuronIndex = 0
    try:
        while True:
            start = line.find("[")
            end = line.find("]")

            if start == -1 or end == -1:
                break

            tempLine = line[start + 1:end].split()
            line = line[end + 1:]
            neuronIndex += 1

            matrixRowPart = [int(x) for x in tempLine]
            matrixRow.append(matrixRowPart)

            if len(matrixRowPart) != vectorLength:
                print(f"Ошибка! Количество компонент нейрона {neuronIndex} в слое {index} ({len(matrixRowPart)}) "
                      f"и размер вектора ({vectorLength}) не совпадают!\n")
                exit()

    except ValueError:
        print(f"Ошибка! Неверный ввод в строке {index}")
        exit()

    matrix.append([matrixRow])

# произведём вычисления

resultMatrix = []

for layer in matrix:
    temp = []
    for part in layer:
        for neuron in part:
            value = 0
            for i in range(len(vector)):
                value += neuron[i] * vector[i]
            value /= 1 + abs(value)
            temp.append(value)
        resultMatrix.append(temp)
        vector = temp

# выведем полученные данные в файл

destination1 = open(destination1Path, "w+")
for x in resultMatrix[-1]:
    destination1.write(str(x) + " ")

network = xml.Element("network")

for layer in matrix:
    tempStr = ""
    for x in layer:
        for y in x:
            tempStr += str(y) + " "
        break
    tempStr = tempStr[:-1]
    xml.SubElement(network, "layer").text = tempStr

    tree = xml.ElementTree(network)
    tree.write(destination2Path)