import itertools
import monde 
import place_holder



class noeud():
    def __init__(self,coord:tuple[int,int],parent=None):
        self.coord = coord
        self.parent = parent





    

def recherche_stupide():
    




    return





def comparairson(n1,n2):
    if n1 >n2:
        return 1
    elif n1 == n2:
        return 0
    else:
        return -1

def evaluer(level:list[list],obj:tuple[int,int])->list[list]:
    d = itertools.product(range(len(level [0])), 
                    range(len(level[0][0])))
    j = [ [ None for y in range(len(level [0][0])) ] for x in range(len(level [0])) ]
    for x,y in d:
        j[x][y] = ( ( obj[0]-x )**2  + ( obj[1]-y )**2) ** (1/2)
      

    return j
    
    
    






def  algoA(nv:list[list],obj)->list:

    """
    implementation de algo Recherche A 

    Args:
        nc (list): le niveau qu'il doit resoudre 
        obj: les coordoné de l'obectif qu'il doit atteindre

    Returns:
        list: la suite action a faire
    """
    d = itertools.product(range(len(nv [0])), 
                      range(len(nv[0][0])))
    tab_eval:list[list] = evaluer(nv,obj)

    solution:list  =[]

    while solution[-1] !=objectif:



        pass


    return solution