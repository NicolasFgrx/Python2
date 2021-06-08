#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

from heapq import *
import io
import os

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
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008 ]
### True chars
def collecte_chars(fichier):
    chars = {}
    f = io.open(fichier, 'r', encoding="utf-8")
    line = f.readline()
    print(line)
    while line:
        for carac in line:
            if chars.get(carac):
                chars[carac] = chars[carac] + 1
            else:
                chars[carac] = 1
        line = f.readline()
    # print(chars)
    chars['EOF'] = 1
    return chars

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
    for etiq, proba in frequences.items():
        feuille = (proba, etiq, Arbre(etiq))
        heappush(tas, feuille)

    #print(tas)

    # creation d'un arbre unique
    while len(tas) > 1:
        item1 = heappop(tas)
        item2 = heappop(tas)
        item3 = (item1[0]+item2[0], item1[1]+item2[1], Arbre(item1[1]+item2[1], item1[2], item2[2]))
        heappush(tas, item3)
    arbre = heappop(tas)
    return arbre[2]


###  Ex.2  construction du code d'Huffamn

def parcours(arbre,prefixe,code) :    
    # à compléter
    if arbre.estFeuille():
        code[arbre.lettre] = prefixe
    if arbre.gauche != None:
        parcours(arbre.gauche, prefixe+"0", code)
    if arbre.droit != None:
        parcours(arbre.droit, prefixe+"1", code)


def code_huffman(arbre):
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(arbre,'',code)
    return code


###  Ex.3  encodage d'un texte contenu dans un fichier

def encodage(dico, fichier):
    f = io.open(fichier, 'r', encoding="utf-8")
    f2 = io.open("leHorlaEncoded.txt", 'wb')
    ligne = f.readline() # premiere ligne
    codeArray = []
    while ligne:
        code = ''

        #parcour les caractères jusqu'a coder toute une ligne :
        for carac in ligne:
            #chercher le code
            code = code + dico.get(carac, dico[' '])

        codeArray.append(code)
        ligne = f.readline()# passe a la ligne suivante

    # code devient une chaine de caractères
    code = ''.join(codeArray)
    #print(code)
    octets = []
    print("code :", code)
    print(len(code)%8)

    code = code + dico.get('EOF')

    # Bourrage  : ajout d'un espace pour retomber sur un multible de 8
    while len(code)%8 != 0:
        code += "0"

    #on regroupe par paquet d'octets
    for i in range(0, len(code), 8):
        octets.append(int(code[i:i+8], 2))


    print(bin(octets[-1]))
    f2.write(bytearray(octets))
    f2.close()
    f.close()

    print(octets)

    orignal_size = os.path.getsize(fichier)
    compress_size = os.path.getsize("leHorlaEncoded.txt")

    print("Taux de compression : ", format((100*(orignal_size-compress_size))/orignal_size,'.2f'), "%")
    return code



###  Ex.4  décodage d'un fichier compresse

def decodage(arbre,fichierCompresse) :
    f = open(fichierCompresse, 'rb')

    byte = f.read(1)

    tampon = ""
    while byte:
        #print(format(bin(byte), '0b'))
        symbole = bin(int.from_bytes(byte, 'big'))
        symbole = str(symbole)
        symbole = symbole[2::]


        while len(symbole) < 8:
            symbole = "0"+symbole

        #print(symbole)
        tampon = tampon + symbole
        byte = f.read(1)
        #bin(int.from_bytes(a, 'big'))[2::]

    f.close()

    print(tampon)
    print(len(tampon))
    texte = ""
    i = 0

    cursor = arbre
    while cursor.lettre != 'EOF':
        cursor = arbre
        while not cursor.estFeuille():
            if tampon[i] == '0':
                cursor = cursor.gauche
            if tampon[i] == '1':
                cursor = cursor.droit
            i += 1
            if cursor.estFeuille():
                if cursor.lettre == 'EOF':
                    return texte
                texte = texte + cursor.lettre

    # return texte


def display(arbre):
    if arbre.estFeuille():
        print(arbre.lettre)
    if arbre.gauche != None:
        display(arbre.gauche)
    if arbre.droit != None:
        display(arbre.droit)

#test = collecte_chars('leHorla.txt')

# F = frequences()
# print(F)
#
# arbre = arbre_huffman(F)
# print(arbre)
#
# dico = code_huffman(arbre)
# print(dico)
# encode = encodage(dico, 'leHorla.txt')
# print("Encode :")
# print(encode)
# print(len(encode))
#
#
# decode = decodage(arbre,'leHorlaEncoded.txt')
# print("Decode :")
# print(decode)
# print(len(decode))



#V2
F2 = collecte_chars("leHorla.txt")
print(F2)

arbre2 = arbre_huffman(F2)
print(arbre2)

dico2 = code_huffman(arbre2)
print(dico2)

encode2 = encodage(dico2, 'leHorla.txt')
print("Encode :")
print(encode2)
print(len(encode2))

decode = decodage(arbre2,'leHorlaEncoded.txt')
print("Decode :")
print(decode)
print(len(decode))




