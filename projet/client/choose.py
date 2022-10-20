# -*- coding: utf-8 -*-

from pprint import pprint
import clauses
import solveur
from crocomine_client import CrocomineClient
import random
    
'''
#à faire : 
    
-chercher autres cas particulier qu'on peut déterminer
- utiliser le nombre d'animaux restants dans les remains au mieux (en partie fait)
- la partie où faut choisir une case au hasard (fait normalement)
- chord?

#quoi en faire?
initialNb_Land = grid_infos['land_count']
initialNb_Sea = grid_infos['sea_count']
index_3BV = grid_infos['3BV']
'''


voc = {'land': 0, 'sea': 1, 'tiger': 2, 'shark': 3 , 'croco': 4}

#choisir discover(), guess() (ou chord())
#renvoie le status de l'action choisie
def chooseAction(grid_infos: dict, knownMap: list, dicoVar :dict,croco: CrocomineClient, clausesBase: list) -> str:
    
    result = ''
    
    height = grid_infos['m']
    width = grid_infos['n']
    
    '''
    dans play.py, on avait :
    grid_infos['remainTiger'] = grid_infos['tiger_count']
    grid_infos['remainShark'] = grid_infos['shark_count']
    grid_infos['remainCroco'] = grid_infos['croco_count']
    ''' 
    
    #si pas de tigres et pas de croco en général...découvrir les terres tout de suite
    if ((grid_infos['remainTiger'] == 0) and (grid_infos['remainCroco'] == 0)):
        for i in range(height):
            for j in range(width):
                caseInfos = knownMap[i][j]
                if ((caseInfos[0] == '.') and (len(caseInfos[1]) == 0) and (caseInfos[2] == '')):
                    status, msg, infos = croco.discover(i, j)
                    print(status, msg)
                    pprint(infos)
                    
                    #à faire mettre à jour la knowMap
                    if (status == 'OK'):
                        for info in infos:
                            i = info['pos'][0]
                            j = info['pos'][1]
                            case = ['?',[],'']
                            field = info['field']
                            if (field == 'land'):
                                case[0] = '.'
                            if (field == 'sea'):
                                case[0] = '~'
                            if ('prox_count' in info): #'prox_count' is optional
                                case[1] = info['prox_count']
                                
                                #donc pas d'animaux dans ces cases données
                                tigerLitteral = clauses.cell_to_variable(i, j, voc['tiger'], dicoVar)
                                sharkLitteral = clauses.cell_to_variable(i, j, voc['shark'], dicoVar)
                                crocoLitteral = clauses.cell_to_variable(i, j, voc['croco'], dicoVar)
                                clausesBase.append(-tigerLitteral)
                                clausesBase.append(-sharkLitteral)
                                clausesBase.append(-crocoLitteral)                                

                            clause = []
                            clause.append(clauses.cell_to_variable(i, j, voc[field], dicoVar))
                            clausesBase += clause 
                                
                            knownMap[i][j] = case                                          
                    
                    return status  

    #si pas de requins et pas de croco en général...découvrir les mers tout de suite
    if ((grid_infos['remainShark'] == 0) and (grid_infos['remainCroco'] == 0)):
        for i in range(height):
            for j in range(width):
                caseInfos = knownMap[i][j]
                if ((caseInfos[0] == '~') and (len(caseInfos[1]) == 0) and (caseInfos[2] == '')):
                    
                    status, msg, infos = croco.discover(i, j) 
                    
                    print(status, msg)
                    pprint(infos)
                    
                    #à faire mettre à jour la knowMap
                    if (status == 'OK'):
                        for info in infos:
                            i = info['pos'][0]
                            j = info['pos'][1]
                            case = ['?',[],'']
                            field = info['field']
                            if (field == 'land'):
                                case[0] = '.'
                            if (field == 'sea'):
                                case[0] = '~'
                            if ('prox_count' in info): #'prox_count' is optional
                                case[1] = info['prox_count']
                                
                                #donc pas d'animaux dans ces cases données
                                tigerLitteral = clauses.cell_to_variable(i, j, voc['tiger'], dicoVar)
                                sharkLitteral = clauses.cell_to_variable(i, j, voc['shark'], dicoVar)
                                crocoLitteral = clauses.cell_to_variable(i, j, voc['croco'], dicoVar)
                                clausesBase.append(-tigerLitteral)
                                clausesBase.append(-sharkLitteral)
                                clausesBase.append(-crocoLitteral)
                                
                            clause = []
                            clause.append(clauses.cell_to_variable(i, j, voc[field], dicoVar))
                            clausesBase += clause  
                                
                            knownMap[i][j] = case
                    
                    return status 
    
    #examiner les cases connues et leur voisinage
    for i in range(height):
        for j in range(width):
            caseInfos = knownMap[i][j]
            if (len(caseInfos[1]) >= 1): #case centrale avec nb tigres, requins et crocos                
                neighborhood = [] #contient des élements de la forme : [i,j,'field',[nbTiger,nbShark,nbCroco],'animal'] ou [i,j,'field',[],'']  
                for neighborPositionLine in [-1,0,1]:
                    for neighborPositionColumn in [-1,0,1]:
                        if not(((neighborPositionLine == 0) and (neighborPositionColumn == 0))): #ne pas ajouter la case elle même dans son voisinage
                            if((0 <= i + neighborPositionLine) and ((height-1) >= i + neighborPositionLine) and (0 <= j + neighborPositionColumn) and ((width-1) >= j + neighborPositionColumn)): #vérifier que la case demandée existe
                                neighborInfos = []
                                neighborInfos.append(i + neighborPositionLine)
                                neighborInfos.append(j + neighborPositionColumn)
                                neighborInfos += knownMap[i + neighborPositionLine][j + neighborPositionColumn]
                                neighborhood.append(neighborInfos)
                                
                for k in neighborhood:
                    if (((k[2] == '.') or (k[2] == '~')) and (len(k[3]) == 0) and k[4] == ''): #si dans l'un des voisins ne possède pas son nb de tigres, requins et crocos mais que l'on sait que son type de terrain alors on examine la case centrale
                        result = examineNeighboorhood(i, j, knownMap,caseInfos,neighborhood,croco, dicoVar, clausesBase, grid_infos) #au moins une case pas encore totalement connue
                        if (result == 'nothing'): #ne pouvait rien déduire
                            break
                        else:
                            return result #le nouveau status   
    
    #choisir ici avec une case inconnue ('?') "au hasard" pour la discover (ou même peut etre guess un animal)
    #return le nouveau status
    tmp=[]
    for i in range(height):
        for j in range(width):
            caseInfos = knownMap[i][j]
            if (caseInfos[0] == '?' or (len(caseInfos[1]) == 0 and caseInfos[2] == '')):
                tmp.append([i,j])
    
                #print("tmp: ",tmp)
    choix=random.choice(tmp)
    #print(choix)
    status, msg, infos = croco.discover(choix[0],choix[1])                
    print(status, msg)
    pprint(infos)               
        
    #à faire mettre à jour la knowMap
    if (status == 'OK'):
        for info in infos:
            i = info['pos'][0]
            j = info['pos'][1]
            case = ['?',[],'']
            field = info['field']
            if (field == 'land'):
                 case[0] = '.'
            if (field == 'sea'):
                 case[0] = '~'
            if ('prox_count' in info): #'prox_count' is optional
                case[1] = info['prox_count']
                            
                #donc pas d'animaux dans ces cases données
                tigerLitteral = clauses.cell_to_variable(i, j, voc['tiger'], dicoVar)
                sharkLitteral = clauses.cell_to_variable(i, j, voc['shark'], dicoVar)
                crocoLitteral = clauses.cell_to_variable(i, j, voc['croco'], dicoVar)
                clausesBase.append(-tigerLitteral)
                clausesBase.append(-sharkLitteral)
                clausesBase.append(-crocoLitteral)                            
                            
            clause = []
            clause.append(clauses.cell_to_variable(i, j, voc[field], dicoVar))
            clausesBase += clause 
                        
            knownMap[i][j] = case
             
            return status    
           
    
    return result

#renvoie le status de l'action choisie ou 'nothing'
#rappel : la liste neighborhood contient des élements de la forme : [i,j,'field',[nbTiger,nbShark,nbCroco],'animal'] ou [i,j,'field',[],'animal'] 
def examineNeighboorhood(column: int, line: int, knownMap: list, caseInfos: list, neighborhood: list,croco: CrocomineClient, dicoVar :dict, clausesBase: list, grid_infos: dict,) -> str:
    
    result = ''
    
    height = grid_infos['m']
    width = grid_infos['n']
    
    nbTigerAround = caseInfos[1][0]
    nbSharkAround = caseInfos[1][1]
    nbCrocoAround = caseInfos[1][2]
    
    #aucun animal ou que des tigres autour donc découvrir une case mer si possible
    if ((nbSharkAround == 0) and (nbCrocoAround == 0)): 
        for neighbor in neighborhood:
            if ((neighbor[2] == '~') and (len(neighbor[3]) == 0)):
                status, msg, infos = croco.discover(neighbor[0], neighbor[1])                
                print(status, msg)
                pprint(infos)
                
                #à faire mettre à jour la knowMap
                if (status == 'OK'):
                    for info in infos:
                        i = info['pos'][0]
                        j = info['pos'][1]
                        case = ['?',[],'']
                        field = info['field']
                        if (field == 'land'):
                            case[0] = '.'
                        if (field == 'sea'):
                            case[0] = '~'
                        if ('prox_count' in info): #'prox_count' is optional
                            case[1] = info['prox_count']
                            
                            #donc pas d'animaux dans ces cases données
                            tigerLitteral = clauses.cell_to_variable(i, j, voc['tiger'], dicoVar)
                            sharkLitteral = clauses.cell_to_variable(i, j, voc['shark'], dicoVar)
                            crocoLitteral = clauses.cell_to_variable(i, j, voc['croco'], dicoVar)
                            clausesBase.append(-tigerLitteral)
                            clausesBase.append(-sharkLitteral)
                            clausesBase.append(-crocoLitteral)                           
                            
                        clause = []
                        clause.append(clauses.cell_to_variable(i, j, voc[field], dicoVar))
                        clausesBase += clause 
                            
                        knownMap[i][j] = case
                
                return status
    
    #aucun animal ou que des requins autour donc découvrir une case terre si possible            
    if ((nbTigerAround == 0) and (nbCrocoAround == 0)): 
        for neighbor in neighborhood:
            if ((neighbor[2] == '.') and (len(neighbor[3]) == 0)):
                status, msg, infos = croco.discover(neighbor[0], neighbor[1])              
                
                print(status, msg)
                pprint(infos)
                
                #à faire mettre à jour la knowMap
                if (status == 'OK'):
                    for info in infos:
                        i = info['pos'][0]
                        j = info['pos'][1]
                        case = ['?',[],'']
                        field = info['field']
                        if (field == 'land'):
                            case[0] = '.'
                        if (field == 'sea'):
                            case[0] = '~'
                        if ('prox_count' in info): #'prox_count' is optional
                            case[1] = info['prox_count']
                            
                            #donc pas d'animaux dans ces cases données
                            tigerLitteral = clauses.cell_to_variable(i, j, voc['tiger'], dicoVar)
                            sharkLitteral = clauses.cell_to_variable(i, j, voc['shark'], dicoVar)
                            crocoLitteral = clauses.cell_to_variable(i, j, voc['croco'], dicoVar)
                            clausesBase.append(-tigerLitteral)
                            clausesBase.append(-sharkLitteral)
                            clausesBase.append(-crocoLitteral)                           

                        clause = []
                        clause.append(clauses.cell_to_variable(i, j, voc[field], dicoVar))
                        clausesBase += clause                             
                            
                        knownMap[i][j] = case
                
                return status
    
    
    #generate problem
    #ici générer les clauses liées au voisinage et les mettres dans la base de clauses       
    clausesBase += clauses.generalConstraints_nbrAnimal([column, line], height, width, [nbTigerAround, nbSharkAround, nbCrocoAround])                        
    
    '''
    Parcourir le voisinage et demander au solveur si dans chaque voisin il y a ou s'il n'y a pas un tigre, un requin ou un crocodile.
    
    si on trouve qu'il n'y a un type d'animal -> discover
    si on trouve qu'il y en a un -> guess
    
    si on ne peut rien déduire -> retourner 'nothing'
    
    '''
    
    #Parcourir le voisinage et envoyer des requêtes au solveur
    for neighbor in neighborhood:
        if (((neighbor[2] == '.') or (neighbor[2] == '~')) and (len(neighbor[3]) == 0)): #si c'est un voisin inconnu mais dont on connait le type de terrain
            
            # 1. demander s'il n'y a aucun animal dans cette case voisine (ni tigre, ni requin, ni crocodile) pour faire un discover
            #utiliser le principe de résolution et de réfutation
            tiger = clauses.cell_to_variable(neighbor[0], neighbor[1], voc['tiger'], dicoVar)
            shark = clauses.cell_to_variable(neighbor[0], neighbor[1], voc['shark'], dicoVar)
            crocodile = clauses.cell_to_variable(neighbor[0], neighbor[1], voc['croco'], dicoVar)
            
            sucessTiger = False
            sucessShark = False
            sucessCrocodile = False

            if (grid_infos['remainTiger'] != 0) :
                clauseTiger = []
                clauseTiger.append(tiger)
                problemClausesTiger = clausesBase + clauseTiger
                sucessTiger = solveur.solve(problemClausesTiger,height,width)
                
            if (grid_infos['remainShark'] != 0) :
                clauseShark = []
                clauseShark.append(shark)
                problemClausesShark = clausesBase + clauseShark
                sucessShark = solveur.solve(problemClausesShark,height,width)
            
            if (grid_infos['remainCroco'] != 0) :
                clauseCrocodile = []
                clauseCrocodile.append(crocodile)
                problemClausesCrocodile = clausesBase + clauseCrocodile
                sucessCrocodile = solveur.solve(problemClausesCrocodile,height,width)
            
            if ((sucessTiger == False) and (sucessShark == False) and (sucessCrocodile == False)):
                caseInfos = knownMap[neighbor[0]][neighbor[1]]
                if (len(caseInfos[1]) == 0): #si pas déjà connue
                
                    status, msg, infos = croco.discover(neighbor[0], neighbor[1])             
                    
                    print(status, msg)
                    pprint(infos)
                    
                    #mettre à jour la knowMap
                    if (status == 'OK'):
                        for info in infos:
                            i = info['pos'][0]
                            j = info['pos'][1]
                            case = ['?',[],'']
                            field = info['field']
                            if (field == 'land'):
                                case[0] = '.'
                            if (field == 'sea'):
                                case[0] = '~'
                            if ('prox_count' in info): #'prox_count' is optional
                                case[1] = info['prox_count']
                                
                                #donc pas d'animaux dans ces cases données
                                tigerLitteral = clauses.cell_to_variable(i, j, voc['tiger'], dicoVar)
                                sharkLitteral = clauses.cell_to_variable(i, j, voc['shark'], dicoVar)
                                crocoLitteral = clauses.cell_to_variable(i, j, voc['croco'], dicoVar)
                                clausesBase.append(-tigerLitteral)
                                clausesBase.append(-sharkLitteral)
                                clausesBase.append(-crocoLitteral)                            
                                
                            knownMap[i][j] = case
                            
                            clause = []
                            clause.append(clauses.cell_to_variable(i, j, voc[field], dicoVar))
                            clausesBase += clause                                   
                    
                    return status  
                #sinon on ne peut rien conclure
            
            
            # 2.demander s'il y a un tigre, un requin ou un crocodile pour faire un guess
            #utiliser le principe de résolution et de réfutation
            
            animalsList = []
            if (grid_infos['remainTiger'] != 0) :
                animalsList.append('tiger')
            if (grid_infos['remainShark'] != 0) :
                animalsList.append('shark')            
            if (grid_infos['remainCroco'] != 0) :
                animalsList.append('croco')   
                
            for animal in animalsList:
                
                #à faire : prendre en compte le nombre de chaque type d'animal à encore trouver
                #en mettant à jour les "remains"                
                
                animalVariable = clauses.cell_to_variable(neighbor[0], neighbor[1], voc[animal], dicoVar)
                
                # non (animal)
                clause = []
                clause.append(-animalVariable)
                
                #tester
                problemClauses = clausesBase + clause
                sucess = solveur.solve(problemClauses,height,width)
                
                
                if (sucess == False):
                    
                    caseInfos = knownMap[neighbor[0]][neighbor[1]]
                    if (len(caseInfos[2]) == 0): #si animal pas déjà connu
                    
                        animalLetter = str
                        if (animal == 'tiger'):
                            animalLetter = "T"
                        if (animal == 'shark'):
                            animalLetter = "S"
                        if (animal == 'croco'):
                            animalLetter = "C" 
                    
                        status, msg, infos = croco.guess(neighbor[0], neighbor[1], animalLetter)
                        print(status, msg)
                        pprint(infos)
                        
                        #mettre à jour la knowMap
                        if (status == 'OK'):
                            
                            #mise à jour du nombre restant d'animaux
                            if ((animal == 'tiger') and (grid_infos['remainTiger'] > 1)):
                                grid_infos['remainTiger'] = grid_infos['remainTiger'] - 1 
                            if ((animal == 'shark') and (grid_infos['remainShark'] > 1)):
                                grid_infos['remainShark'] =  grid_infos['remainShark'] - 1
                            if ((animal == 'croco') and (grid_infos['remainCroco'] > 1)):
                                grid_infos['remainCroco'] = grid_infos['remainCroco'] - 1                            

                            
                            for info in infos:
                                i = info['pos'][0]
                                j = info['pos'][1]
                                case = ['?',[],'']
                                field = info['field']
                                if (field == 'land'):
                                    case[0] = '.'
                                if (field == 'sea'):
                                    case[0] = '~'
                                if ('prox_count' in info): #'prox_count' is optional
                                    case[1] = info['prox_count']
                                    
                                    #donc pas d'animaux dans ces cases données
                                    tigerLitteral = clauses.cell_to_variable(i, j, voc['tiger'], dicoVar)
                                    sharkLitteral = clauses.cell_to_variable(i, j, voc['shark'], dicoVar)
                                    crocoLitteral = clauses.cell_to_variable(i, j, voc['croco'], dicoVar)
                                    clausesBase.append(-tigerLitteral)
                                    clausesBase.append(-sharkLitteral)
                                    clausesBase.append(-crocoLitteral)                                  
                                    
                                knownMap[i][j] = case
                                
                                clause = []
                                clause.append(clauses.cell_to_variable(i, j, voc[field], dicoVar))
                                clausesBase += clause                             

                            clause = []
                            clause.append(clauses.cell_to_variable(neighbor[0], neighbor[1], voc[animal], dicoVar))
                            clausesBase += clause
                            
                            knownMap[neighbor[0]][neighbor[1]][2] = animalLetter
                            
                        return status  
                
                #sinon on ne peut rien conclure
                else:
                    result = "nothing"          

    return result
