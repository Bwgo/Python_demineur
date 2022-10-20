# -*- coding: utf-8 -*-
from typing import List, Tuple
from itertools import combinations


voc = {"land": 0, "sea": 1, "tiger": 2, "shark": 3, "croco": 4}

# dico['i,j,value'] = variable
def generation_dicoVar(height: int, width: int) -> dict:
    counter = 1
    dico = {}
    for i in range(height):
        for j in range(width):
            for value in range(5):  # longueur du dictionnaire de vocabulaire
                key = str(i) + "," + str(j) + "," + str(value)
                dico[key] = counter
                counter += 1
    return dico


def cell_to_variable(i: int, j: int, value: int, dicoVar: dict) -> int:
    key = str(i) + "," + str(j) + "," + str(value)
    return dicoVar[key]


def variable_to_cell(var: int, dicoVar: dict) -> Tuple[int, int, int]:
    T = []
    dicoVar_valuesList = list(dicoVar.values())
    dicoVar_keyList = list(dicoVar.keys())
    position = dicoVar_valuesList.index(var)
    variable = dicoVar_keyList[position]
    listVariableContent = variable.split(",")  # liste de la forme ['i','j','value']
    i = int(listVariableContent[0])
    j = int(listVariableContent[1])
    value = int(listVariableContent[2])
    T.append(i)
    T.append(j)
    T.append(value)
    return T


def non(e: int) -> int:
    return -e


# Contrainte 1: Une case est soit de type terrestre, soit de type aquatique (OU exlcusif)
# Entrée: la taille de la grille (m,n) et le dictionnaire des variables
def generalConstraints_landOrSea(m: int, n: int, dicoVar: dict) -> List[List[int]]:
    L = []
    for i in range(m):
        for j in range(n):
            land = cell_to_variable(i, j, voc["land"], dicoVar)
            sea = cell_to_variable(i, j, voc["sea"], dicoVar)
            L.append([land, sea])
            L.append([non(land), non(sea)])
    return L


# Contrainte2: Dans une case il y a au plus un animal
def generalConstraints_maxOneAnimal(m: int, n: int, dicoVar: dict) -> List[List[int]]:
    L = []
    for i in range(m):
        for j in range(n):
            tiger = cell_to_variable(i, j, voc["tiger"], dicoVar)
            shark = cell_to_variable(i, j, voc["shark"], dicoVar)
            croco = cell_to_variable(i, j, voc["croco"], dicoVar)
            L.append([non(shark), non(croco)])
            L.append([non(tiger), non(croco)])
            L.append([non(tiger), non(shark)])
    return L


# print(generalConstraints_maxOneAnimal(2,5,generation_dicoVar(2,5)))

# Contrainte3: Tigre -> Terre cad nonTigre ou Terre
#             Requin -> Mer cad nonRequin ou Mer
def generalConstraints_animalField(m: int, n: int, dicoVar: dict) -> List[List[int]]:
    L = []
    for i in range(m):
        for j in range(n):
            land = cell_to_variable(i, j, voc["land"], dicoVar)
            sea = cell_to_variable(i, j, voc["sea"], dicoVar)
            tiger = cell_to_variable(i, j, voc["tiger"], dicoVar)
            shark = cell_to_variable(i, j, voc["shark"], dicoVar)
            L.append([non(tiger), land])
            L.append([non(shark), sea])
    return L


def at_least_n_8(n: int, vars: List[int]) -> List[int]:
    r = []
    for hello in combinations(vars, 9 - n):
        r.append(list(hello))
    return r


def n_ique_8(n: int, vars: List[int]) -> List[List[int]]:
    r = at_least_n_8(n, vars)
    oppVars = [(-val) for val in vars]
    for comb in combinations(oppVars, n + 1):
        r.append(list(comb))
    res = [x for x in r if x]
    return res


######################################
# En suite on traite les cases au coins ( qui a que 3 voisins)
######################################


def at_least_n_3(n: int, vars: List[int]) -> List[int]:
    r = []
    for hello in combinations(vars, 4 - n):
        r.append(list(hello))
    return r


def n_ique_3(n: int, vars: List[int]) -> List[List[int]]:
    r = at_least_n_3(n, vars)
    oppVars = [(-val) for val in vars]
    for comb in combinations(oppVars, n + 1):
        r.append(list(comb))
    res = [x for x in r if x]
    return res


######################################
# En suite on traite les cases sur les côtés ( qui a que 5 voisins)
######################################
def at_least_n_5(n: int, vars: List[int]) -> List[int]:
    r = []
    for hello in combinations(vars, 6 - n):
        r.append(list(hello))
    return r


def n_ique_5(n: int, vars: List[int]) -> List[List[int]]:
    r = at_least_n_5(n, vars)
    oppVars = [(-val) for val in vars]
    for comb in combinations(oppVars, n + 1):
        r.append(list(comb))
    res = [x for x in r if x]
    return res


# Contrainte4: Pour une case au milieu, dans son infos on a "prox_count": (n1:int, n2:int, n3:int)
# c-a-d elle a EXACTEMENT n1 voisins tigre, n2 voisins requin, n3 voisins crocodile
def eight(L: List[int], count: int) -> List[List[int]]:
    L1 = []
    if count == 0:  # il n'existe aucun tiger dans son voisinage
        for var in L:
            L1.append([non(var)])
    elif count == 1:
        L1 = n_ique_8(1,L)
    elif count == 2:
        L1 = n_ique_8(2,L)
    elif count == 3:
        L1 = n_ique_8(3,L)
    elif count == 4:
        L1 = n_ique_8(4,L)
    elif count == 5:
        L1 = n_ique_8(5,L)
    elif count == 6:
        L1 = n_ique_8(6,L)
    elif count == 7:
        L1 = n_ique_8(7,L)
    elif count == 8:
        for var in L:
            L1.append([var])
    return L1

#print(eight([1,2,3,4,5,6,7,8],3))

def five(L: List[int], count: int) -> List[List[int]]:
    L1 = []
    if count == 0:
        for var in L:
            L1.append([non(var)])
    elif count == 1:
        L1 = n_ique_5(1,L)
    elif count == 2:
        L1 = n_ique_5(2,L)
    elif count == 3:
        L1 = n_ique_5(3,L)
    elif count == 4:
        L1 = n_ique_5(4,L)
    elif count == 5:
        for var in L:
            L1.append([var])
    return L1


def three(L: List[int], count: int) -> List[List[int]]:
    L1 = []
    if count == 0:
        for var in L:
            L1.append([non(var)])
    elif count == 1:
        L1 = n_ique_3(1,L)
    elif count == 2:
        L1 = n_ique_3(2,L)
    elif count == 3:
        for var in L:
            L1.append([var])
    return L1


def generalConstraints_nbrAnimal(
    position: List[int], m: int, n: int, count: List[int]
) -> List[List[int]]:
    dicoVar = generation_dicoVar(m, n)

    if (
        position[0] > 0
        and position[0] < m - 1
        and position[1] > 0
        and position[1] < n - 1
    ):

        # case au milieu
        leftT = cell_to_variable(position[0], position[1] - 1, 2, dicoVar)
        rightT = cell_to_variable(position[0], position[1] + 1, 2, dicoVar)
        upT = cell_to_variable(position[0] - 1, position[1], 2, dicoVar)
        downT = cell_to_variable(position[0] + 1, position[1], 2, dicoVar)
        upperleftT = cell_to_variable(position[0] - 1, position[1] - 1, 2, dicoVar)
        upperrightT = cell_to_variable(position[0] - 1, position[1] + 1, 2, dicoVar)
        lowerleftT = cell_to_variable(position[0] + 1, position[1] - 1, 2, dicoVar)
        lowerrightT = cell_to_variable(position[0] + 1, position[1] + 1, 2, dicoVar)

        leftS = cell_to_variable(position[0], position[1] - 1, 3, dicoVar)
        rightS = cell_to_variable(position[0], position[1] + 1, 3, dicoVar)
        upS = cell_to_variable(position[0] - 1, position[1], 3, dicoVar)
        downS = cell_to_variable(position[0] + 1, position[1], 3, dicoVar)
        upperleftS = cell_to_variable(position[0] - 1, position[1] - 1, 3, dicoVar)
        upperrightS = cell_to_variable(position[0] - 1, position[1] + 1, 3, dicoVar)
        lowerleftS = cell_to_variable(position[0] + 1, position[1] - 1, 3, dicoVar)
        lowerrightS = cell_to_variable(position[0] + 1, position[1] + 1, 3, dicoVar)

        leftC = cell_to_variable(position[0], position[1] - 1, 4, dicoVar)
        rightC = cell_to_variable(position[0], position[1] + 1, 4, dicoVar)
        upC = cell_to_variable(position[0] - 1, position[1], 4, dicoVar)
        downC = cell_to_variable(position[0] + 1, position[1], 4, dicoVar)
        upperleftC = cell_to_variable(position[0] - 1, position[1] - 1, 4, dicoVar)
        upperrightC = cell_to_variable(position[0] - 1, position[1] + 1, 4, dicoVar)
        lowerleftC = cell_to_variable(position[0] + 1, position[1] - 1, 4, dicoVar)
        lowerrightC = cell_to_variable(position[0] + 1, position[1] + 1, 4, dicoVar)

        LTiger = []
        LTiger.append(leftT)
        LTiger.append(rightT)
        LTiger.append(upT)
        LTiger.append(downT)
        LTiger.append(upperleftT)
        LTiger.append(upperrightT)
        LTiger.append(lowerleftT)
        LTiger.append(lowerrightT)
        L1 = eight(LTiger, count[0])

        LShark = []
        LShark.append(leftS)
        LShark.append(rightS)
        LShark.append(upS)
        LShark.append(downS)
        LShark.append(upperleftS)
        LShark.append(upperrightS)
        LShark.append(lowerleftS)
        LShark.append(lowerrightS)
        L2 = eight(LShark, count[1])

        LCroco = []
        LCroco.append(leftC)
        LCroco.append(rightC)
        LCroco.append(upC)
        LCroco.append(downC)
        LCroco.append(upperleftC)
        LCroco.append(upperrightC)
        LCroco.append(lowerleftC)
        LCroco.append(lowerrightC)
        L3 = eight(LCroco, count[2])

    elif position[0] == 0 and position[1] == 0:
        # Coin supérieur gauche

        rightT = cell_to_variable(position[0], position[1] + 1, 2, dicoVar)
        downT = cell_to_variable(position[0] + 1, position[1], 2, dicoVar)
        lowerrightT = cell_to_variable(position[0] + 1, position[1] + 1, 2, dicoVar)

        rightS = cell_to_variable(position[0], position[1] + 1, 3, dicoVar)
        downS = cell_to_variable(position[0] + 1, position[1], 3, dicoVar)
        lowerrightS = cell_to_variable(position[0] + 1, position[1] + 1, 3, dicoVar)

        rightC = cell_to_variable(position[0], position[1] + 1, 4, dicoVar)
        downC = cell_to_variable(position[0] + 1, position[1], 4, dicoVar)
        lowerrightC = cell_to_variable(position[0] + 1, position[1] + 1, 4, dicoVar)

        LTiger = []
        LTiger.append(rightT)
        LTiger.append(downT)
        LTiger.append(lowerrightT)
        L1 = three(LTiger, count[0])

        LShark = []
        LShark.append(rightS)
        LShark.append(downS)
        LShark.append(lowerrightS)
        L2 = three(LShark, count[1])

        LCroco = []
        LCroco.append(rightC)
        LCroco.append(downC)
        LCroco.append(lowerrightC)
        L3 = three(LCroco, count[2])

    elif position[0] == m - 1 and position[1] == n - 1:
        # coin en bas à droite

        leftT = cell_to_variable(position[0], position[1] - 1, 2, dicoVar)
        upT = cell_to_variable(position[0] - 1, position[1], 2, dicoVar)
        upperleftT = cell_to_variable(position[0] - 1, position[1] - 1, 2, dicoVar)

        leftS = cell_to_variable(position[0], position[1] - 1, 3, dicoVar)
        upS = cell_to_variable(position[0] - 1, position[1], 3, dicoVar)
        upperleftS = cell_to_variable(position[0] - 1, position[1] - 1, 3, dicoVar)

        leftC = cell_to_variable(position[0], position[1] - 1, 4, dicoVar)
        upC = cell_to_variable(position[0] - 1, position[1], 4, dicoVar)
        upperleftC = cell_to_variable(position[0] - 1, position[1] - 1, 4, dicoVar)

        LTiger = []
        LTiger.append(leftT)
        LTiger.append(upT)
        LTiger.append(upperleftT)
        L1 = three(LTiger, count[0])

        LShark = []
        LShark.append(leftS)
        LShark.append(upS)
        LShark.append(upperleftS)
        L2 = three(LShark, count[1])

        LCroco = []
        LCroco.append(leftC)
        LCroco.append(upC)
        LCroco.append(upperleftC)
        L3 = three(LCroco, count[2])

    elif position[0] == 0 and position[1] == n - 1:
        # coin en haut à droite

        leftT = cell_to_variable(position[0], position[1] - 1, 2, dicoVar)
        downT = cell_to_variable(position[0] + 1, position[1], 2, dicoVar)
        lowerleftT = cell_to_variable(position[0] + 1, position[1] - 1, 2, dicoVar)

        leftS = cell_to_variable(position[0], position[1] - 1, 2, dicoVar)
        downS = cell_to_variable(position[0] + 1, position[1], 3, dicoVar)
        lowerleftS = cell_to_variable(position[0] + 1, position[1] - 1, 3, dicoVar)

        leftC = cell_to_variable(position[0], position[1] - 1, 4, dicoVar)
        downC = cell_to_variable(position[0] + 1, position[1], 4, dicoVar)
        lowerleftC = cell_to_variable(position[0] + 1, position[1] - 1, 4, dicoVar)

        LTiger = []
        LTiger.append(leftT)
        LTiger.append(downT)
        LTiger.append(lowerleftT)
        L1 = three(LTiger, count[0])

        LShark = []
        LShark.append(leftS)
        LShark.append(downS)
        LShark.append(lowerleftS)
        L2 = three(LShark, count[1])

        LCroco = []
        LCroco.append(leftC)
        LCroco.append(downC)
        LCroco.append(lowerleftC)
        L3 = three(LCroco, count[2])

    elif position[0] == m - 1 and position[1] == 0:
        # coin en bas à gauche

        rightT = cell_to_variable(position[0], position[1] + 1, 2, dicoVar)
        upT = cell_to_variable(position[0] - 1, position[1], 2, dicoVar)
        upperrightT = cell_to_variable(position[0] - 1, position[1] + 1, 2, dicoVar)

        rightS = cell_to_variable(position[0], position[1] + 1, 3, dicoVar)
        upS = cell_to_variable(position[0] - 1, position[1], 3, dicoVar)
        upperrightS = cell_to_variable(position[0] - 1, position[1] + 1, 3, dicoVar)

        rightC = cell_to_variable(position[0], position[1] + 1, 4, dicoVar)
        upC = cell_to_variable(position[0] - 1, position[1], 4, dicoVar)
        upperrightC = cell_to_variable(position[0] - 1, position[1] + 1, 4, dicoVar)

        LTiger = []
        LTiger.append(rightT)
        LTiger.append(upT)
        LTiger.append(upperrightT)
        L1 = three(LTiger, count[0])

        LShark = []
        LShark.append(rightS)
        LShark.append(upS)
        LShark.append(upperrightS)
        L2 = three(LShark, count[1])

        LCroco = []
        LCroco.append(rightS)
        LCroco.append(upS)
        LCroco.append(upperrightS)
        L3 = three(LCroco, count[2])

    elif position[0] == 0 and position[1] > 0 and position[1] < n - 1:

        leftT = cell_to_variable(position[0], position[1] - 1, 2, dicoVar)
        rightT = cell_to_variable(position[0], position[1] + 1, 2, dicoVar)
        downT = cell_to_variable(position[0] + 1, position[1], 2, dicoVar)
        lowerleftT = cell_to_variable(position[0] + 1, position[1] - 1, 2, dicoVar)
        lowerrightT = cell_to_variable(position[0] + 1, position[1] + 1, 2, dicoVar)

        leftS = cell_to_variable(position[0], position[1] - 1, 3, dicoVar)
        rightS = cell_to_variable(position[0], position[1] + 1, 3, dicoVar)
        downS = cell_to_variable(position[0] + 1, position[1], 3, dicoVar)
        lowerleftS = cell_to_variable(position[0] + 1, position[1] - 1, 3, dicoVar)
        lowerrightS = cell_to_variable(position[0] + 1, position[1] + 1, 3, dicoVar)

        leftC = cell_to_variable(position[0], position[1] - 1, 4, dicoVar)
        rightC = cell_to_variable(position[0], position[1] + 1, 4, dicoVar)
        downC = cell_to_variable(position[0] + 1, position[1], 4, dicoVar)
        lowerleftC = cell_to_variable(position[0] + 1, position[1] - 1, 4, dicoVar)
        lowerrightC = cell_to_variable(position[0] + 1, position[1] + 1, 4, dicoVar)

        LTiger = []
        LTiger.append(leftT)
        LTiger.append(rightT)
        LTiger.append(downT)
        LTiger.append(lowerleftT)
        LTiger.append(lowerrightT)
        L1 = five(LTiger, count[0])

        LShark = []
        LShark.append(leftS)
        LShark.append(rightS)
        LShark.append(downS)
        LShark.append(lowerleftS)
        LShark.append(lowerrightS)
        L2 = five(LShark, count[1])

        LCroco = []
        LCroco.append(leftC)
        LCroco.append(rightC)
        LCroco.append(downC)
        LCroco.append(lowerleftC)
        LCroco.append(lowerrightC)
        L3 = five(LCroco, count[2])

    elif position[0] == m - 1 and position[1] > 0 and position[1] < n - 1:

        leftT = cell_to_variable(position[0], position[1] - 1, 2, dicoVar)
        rightT = cell_to_variable(position[0], position[1] + 1, 2, dicoVar)
        upT = cell_to_variable(position[0] - 1, position[1], 2, dicoVar)
        upperleftT = cell_to_variable(position[0] - 1, position[1] - 1, 2, dicoVar)
        upperrightT = cell_to_variable(position[0] - 1, position[1] + 1, 2, dicoVar)

        leftS = cell_to_variable(position[0], position[1] - 1, 3, dicoVar)
        rightS = cell_to_variable(position[0], position[1] + 1, 3, dicoVar)
        upS = cell_to_variable(position[0] - 1, position[1], 3, dicoVar)
        upperleftS = cell_to_variable(position[0] - 1, position[1] - 1, 3, dicoVar)
        upperrightS = cell_to_variable(position[0] - 1, position[1] + 1, 3, dicoVar)

        leftC = cell_to_variable(position[0], position[1] - 1, 4, dicoVar)
        rightC = cell_to_variable(position[0], position[1] + 1, 4, dicoVar)
        upC = cell_to_variable(position[0] - 1, position[1], 4, dicoVar)
        upperleftC = cell_to_variable(position[0] - 1, position[1] - 1, 4, dicoVar)
        upperrightC = cell_to_variable(position[0] - 1, position[1] + 1, 4, dicoVar)

        LTiger = []
        LTiger.append(leftT)
        LTiger.append(rightT)
        LTiger.append(upT)
        LTiger.append(upperleftT)
        LTiger.append(upperrightT)
        L1 = five(LTiger, count[0])

        LShark = []
        LShark.append(leftS)
        LShark.append(rightS)
        LShark.append(upS)
        LShark.append(upperleftS)
        LShark.append(upperrightS)
        L2 = five(LShark, count[1])

        LCroco = []
        LCroco.append(leftC)
        LCroco.append(rightC)
        LCroco.append(upC)
        LCroco.append(upperleftC)
        LCroco.append(upperrightC)
        L3 = five(LCroco, count[2])

    elif position[0] > 0 and position[0] < m - 1 and position[1] == 0:

        rightT = cell_to_variable(position[0], position[1] + 1, 2, dicoVar)
        upT = cell_to_variable(position[0] - 1, position[1], 2, dicoVar)
        downT = cell_to_variable(position[0] + 1, position[1], 2, dicoVar)
        upperrightT = cell_to_variable(position[0] - 1, position[1] + 1, 2, dicoVar)
        lowerrightT = cell_to_variable(position[0] + 1, position[1] + 1, 2, dicoVar)

        rightS = cell_to_variable(position[0], position[1] + 1, 3, dicoVar)
        upS = cell_to_variable(position[0] - 1, position[1], 3, dicoVar)
        downS = cell_to_variable(position[0] + 1, position[1], 3, dicoVar)
        upperrightS = cell_to_variable(position[0] - 1, position[1] + 1, 3, dicoVar)
        lowerrightS = cell_to_variable(position[0] + 1, position[1] + 1, 3, dicoVar)

        rightC = cell_to_variable(position[0], position[1] + 1, 4, dicoVar)
        upC = cell_to_variable(position[0] - 1, position[1], 4, dicoVar)
        downC = cell_to_variable(position[0] + 1, position[1], 4, dicoVar)
        upperrightC = cell_to_variable(position[0] - 1, position[1] + 1, 4, dicoVar)
        lowerrightC = cell_to_variable(position[0] + 1, position[1] + 1, 4, dicoVar)

        LTiger = []
        LTiger.append(rightT)
        LTiger.append(upT)
        LTiger.append(downT)
        LTiger.append(upperrightT)
        LTiger.append(lowerrightT)
        L1 = five(LTiger, count[0])

        LShark = []
        LShark.append(rightS)
        LShark.append(upS)
        LShark.append(downS)
        LShark.append(upperrightS)
        LShark.append(lowerrightS)
        L2 = five(LShark, count[1])

        LCroco = []
        LCroco.append(rightC)
        LCroco.append(upC)
        LCroco.append(downC)
        LCroco.append(upperrightC)
        LCroco.append(lowerrightC)
        L3 = five(LCroco, count[2])

    elif position[0] > 0 and position[0] < m - 1 and position[1] == n - 1:
        leftT = cell_to_variable(position[0], position[1] - 1, 2, dicoVar)
        upT = cell_to_variable(position[0] - 1, position[1], 2, dicoVar)
        downT = cell_to_variable(position[0] + 1, position[1], 2, dicoVar)
        upperleftT = cell_to_variable(position[0] - 1, position[1] - 1, 2, dicoVar)
        lowerleftT = cell_to_variable(position[0] + 1, position[1] - 1, 2, dicoVar)

        leftS = cell_to_variable(position[0], position[1] - 1, 3, dicoVar)
        upS = cell_to_variable(position[0] - 1, position[1], 3, dicoVar)
        downS = cell_to_variable(position[0] + 1, position[1], 3, dicoVar)
        upperleftS = cell_to_variable(position[0] - 1, position[1] - 1, 3, dicoVar)
        lowerleftS = cell_to_variable(position[0] + 1, position[1] - 1, 3, dicoVar)

        leftC = cell_to_variable(position[0], position[1] - 1, 4, dicoVar)
        upC = cell_to_variable(position[0] - 1, position[1], 4, dicoVar)
        downC = cell_to_variable(position[0] + 1, position[1], 4, dicoVar)
        upperleftC = cell_to_variable(position[0] - 1, position[1] - 1, 4, dicoVar)
        lowerleftC = cell_to_variable(position[0] + 1, position[1] - 1, 4, dicoVar)

        LTiger = []
        LTiger.append(leftT)
        LTiger.append(upT)
        LTiger.append(downT)
        LTiger.append(upperleftT)
        LTiger.append(lowerleftT)
        L1 = five(LTiger, count[0])

        LShark = []
        LShark.append(leftS)
        LShark.append(upS)
        LShark.append(downS)
        LShark.append(upperleftS)
        LShark.append(lowerleftS)
        L2 = five(LShark, count[1])

        LCroco = []
        LCroco.append(leftC)
        LCroco.append(upC)
        LCroco.append(downC)
        LCroco.append(upperleftC)
        LCroco.append(lowerleftC)
        L3 = five(LCroco, count[2])

    return L1 + L2 + L3


# L = generalConstraints_nbrAnimal([1, 2], 3, 3, [1, 1, 1])
# print(L)

