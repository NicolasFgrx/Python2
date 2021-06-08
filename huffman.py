#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

from heapq import *

###  distribution de proba sur les letrres

caracteres = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z' ]

proba = [
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008  ]

tas = []
heapify(tas)

def frequences() :
    table = {}
    n = len(caracteres)
    for i in range(n):
        table[caracteres[i]] = proba[i]
    return table



###  la classe Arbre

class Arbre :
    def __init__(self, lettre, gauche=None, droit=None):
        self.gauche=gauche
        self.droit=droit
        self.lettre=lettre
    def estFeuille(self):
        return self.gauche == None and self.droit == None
    def estVide(self):
        return self == None
    def __str__(self):
        return '<'+ str(self.lettre)+'.'+str(self.gauche)+'.'+str(self.droit)+'>'


###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
def arbre_huffman(frequences) :
    # création des feuilles
    for etiq, freq in frequences.items():
        feuille = (freq, etiq, Arbre(etiq))
        heappush(tas, feuille)

    # creation d'un arbre unique
    while len(tas) >= 2:
        item1 = heappop(tas)
        item2 = heappop(tas)
        # print("item 1 : ", item1)
        # print("item 2 : ", item2)
        item3 = (item1[0]+item2[0], item1[1]+item2[1], Arbre(item1[1]+item2[1], item1, item2))
        # print("item 3 : ", item3)
        heappush(tas, item3)
    arbre = heappop(tas)
    return arbre


###  Ex.2  construction du code d'Huffamn

def parcours(arbre,prefixe,code) :    
    # à compléter
    if arbre.estFeuille():
            code[arbre.lettre] = prefixe
    if arbre.gauche != None:
        parcours(arbre.gauche, prefixe+"0", code)
    if arbre.droit != None:
        parcours(arbre.droit, prefixe+"1", code)


def code_huffman(arbre) :
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(arbre,'',code)
    return code

###  Ex.3  encodage d'un texte contenu dans un fichier

def encodage(dico,fichier) :
    # à compléter
    print()

###  Ex.4  décodage d'un fichier compresse

def decodage(arbre,fichierCompresse) :
    # à compléter
    print()

F = frequences()
print(F)

tas = arbre_huffman(F)
print(tas)

dictionnaire = code_huffman(tas)
print(dictionnaire)

#encode = encodage(dico, 'leHorla.txt')
#print(encode)
#decode = decodage(H,'leHorlaEncoded.txt')
#print(decode)
