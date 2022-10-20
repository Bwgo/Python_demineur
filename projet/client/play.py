# -*- coding: utf-8 -*-

'''
Projet Final IA02 : Jeu du démineur avec des tigres, des requins et des crocodiles.
Groupe 13 : Aurélie Law-Yen et Yanan Fu.
'''

from pprint import pprint
from crocomine_client import CrocomineClient
import clauses
from choose import chooseAction

voc = {'land': 0, 'sea': 1, 'tiger': 2, 'shark': 3 , 'croco': 4}

def play():
    
    server = "http://localhost:8000"
    group = "Groupe 13"
    members = "Aurélie LAW-YEN et Yanan FU"
    croco = CrocomineClient(server, group, members)    
    
    continueToPlay = True
    while (continueToPlay):
        status, msg, grid_infos = croco.new_grid()
        print(status, msg)
        pprint(grid_infos)
        
        if (status == 'OK'):
            status = playTheNewGrid(grid_infos, croco)
        '''
            if (status == 'Err'):
               continueToPlay = False
      
            if (status == 'KO'):
                continueToPlay = False
           
        if (status == 'Err'):
            continueToPlay = False
        
        if (status == 'KO'):
            continueToPlay = False
            #print("Il n’y a plus de grille.")
        '''
    return   
            

def playTheNewGrid(grid_infos: dict, croco: CrocomineClient):
    
    height = grid_infos['m']
    width = grid_infos['n']
    start = grid_infos['start']  #safe case
    initialInfos = grid_infos['infos'] #optional
    
    clausesBase = []
    
    dicoVar = clauses.generation_dicoVar(height, width)
    
    knownMap = []
    for i in range(height):
        lineKnownMap = []
        for j in range(width):
            unknownCase = ['?',[],'']
            lineKnownMap.append(unknownCase)
        knownMap.append(lineKnownMap)
        
    #add given initial informations into our knownMap
    for info in initialInfos:
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
        knownMap[i][j] = case
    
    #normally 'start' is a safe case
    status, msg, infos = croco.discover(start[0],start[1])
    
    if (status == 'GG'):
        print(msg, status)
        pprint(grid_infos)

    if (status == 'Err'):
        print(msg, status)
        pprint(grid_infos)          
    
    if (status == 'KO'):
        print("La case de départ n'était pas sûre.")
        print(msg, status)
        pprint(grid_infos)
    
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
            
        status = playCurrent(grid_infos, knownMap, croco, clausesBase, dicoVar)
            
    return status
     

def playCurrent(grid_infos: dict, knownMap: list, croco: CrocomineClient, clausesBase: list, dicoVar :dict):

    height = grid_infos['m']
    width = grid_infos['n']
        
    #générer ici clauses générales
    clausesBase += clauses.generalConstraints_landOrSea(height, width, dicoVar)
    clausesBase += clauses.generalConstraints_maxOneAnimal(height, width, dicoVar)
    clausesBase += clauses.generalConstraints_animalField(height, width, dicoVar)
    
    #combien il reste d'animaux à trouver
    grid_infos['remainTiger'] = grid_infos['tiger_count']
    grid_infos['remainShark'] = grid_infos['shark_count']
    grid_infos['remainCroco'] = grid_infos['croco_count']
        
    status = 'OK'
    while (status == 'OK'):
        
        status = chooseAction(grid_infos, knownMap, dicoVar, croco, clausesBase)
        
    return status


if __name__ == "__main__":
    play()
