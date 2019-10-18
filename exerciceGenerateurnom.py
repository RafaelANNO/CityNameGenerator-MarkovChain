"""
author: ANNO Rafael
"""
import csv
import random as random
import os
import datetime

"""
Les mathématiques discrètes, parfois appelées mathématiques finies, sont
l'étude des structures mathématiques fondamentalement discrètes, par
opposition aux structures continues. Contrairement aux nombres réels,
qui ont la propriété de varier "en douceur", les objets étudiés en
mathématiques discrètes (tels que les entiers relatifs, les graphes
simples et les énoncés en logique1) ne varient pas de cette façon,
mais ont des valeurs distinctes séparées.

La notion de propriété markovienne définit une classe de processus
discrets ou continus, à valeurs discrètes ou continues, qui repose
sur l'hypothèse selon laquelle l'avenir ne dépend que de l'instant
présent.
"""
def build_markov_chain(data, n):
    """
        Cette fonction permet de generer une chaine
        de markov(chaine respectant la lotion de propriété markovienne)
        depuis data à la position n. Ici notre chaine de markov est une
        liste d'éléments qui sont associer à d'autres éléments qui sont
        susceptibles d'apparaitre juste apres ce même élément.
        (exemple de structure avec n = 5: Pari => 's' => nombre de fois que s est apparu apres la chaine Pari)
        Notre chaine de markov constituera une phase d'apprentissage pendant laquel elle va etablir la 
        liste des éléments qui peuvent suivre chaque element avec leurs probabilité
        Exemple profond des chaines de markov : http://setosa.io/ev/markov-chains/
        
        :param data       : La liste des données existantes dans cette liste on associe des mots parents à un
            autres tableau associatif qui associe des mots pouvant suivre le mot parent et le nombre 
            d'occurences trouvées pour le mot associé
        :type data        : list
        :param n          : La position à laquelle nous voulons étudier le comportement des mots
        :type data        : int
    """
    chain = {
        # Initial est le dictionnaire qui contient tous les enchainements possibles
        '_initial': {},
        # Name contient le nom des communes
        '_names'  : set(data)
    }
    for word in data:
        word_wrapped = str(word) + '.'
        for i in range(0, len(word_wrapped) - n):
            tuple = word_wrapped[i:i + n]
            next = word_wrapped[i + 1:i + n + 1]
            
            if tuple not in chain:
                entry = chain[tuple] = {}
            else:
                entry = chain[tuple]
            
            if i == 0:
                if tuple not in chain['_initial']:
                    chain['_initial'][tuple] = 1
                else:
                    chain['_initial'][tuple] += 1
            
            if next not in entry:
                entry[next] = 1
            else:
                entry[next] += 1
    return chain

def select_random_item(items):
    """
        Selectionne au hazard un item contenu contenu dans items en
        suivants les regles de probabilité spécifiées sous form de 
        chaine de markov
    """
    rnd = random.random() * sum(items.values())
    for item in items:
        rnd -= items[item]
        if rnd < 0:
            return item
        
def generate(chain, debut_de_mot = None, taille = None):
    """
        Permet de generer une chaine de caractere à partir 
        d'une chaine de Markov
        :param chain        : La chaine de markov representant les fréquences d'apparition des lettre
        :param debut_de_mot : Le debut de mot souhaité (peut être null)
        :type debut_de_mot  : str
        :param taille       : La taille du mot souhaité (peut être null)
        :type a             : int
        :return             : The name generated
        :rtype              : str
    """
    while True:
        err_type = ''
        if not(debut_de_mot is None) and not(type(debut_de_mot) is str):
            err_type+='\n Le début de mot doit être un string'
        if not(taille is None) and not(type(taille) is int):
            err_type+='\n La taille doit être un int'
        if err_type!='':
            raise TypeError(err_type)
            break
        err_combined_param = ''
        if not(debut_de_mot is None) and not(taille is None):
            if (len(debut_de_mot) >= taille) or (taille <= 0):
                err_combined_param += '\n la taille de debut de mot est superieur ou egale à la taille souhaitée'
        if err_combined_param != '':
            raise ValueError(err_combined_param)
            break
        break
            
    tuple  = select_random_item(chain['_initial'])
    if debut_de_mot is None:
        result = [tuple]
    else:
        result = [debut_de_mot]
    while True:
        tuple = select_random_item(chain[tuple])
        last_character = tuple[-1]
        if last_character == '.':
            break
        result.append(last_character)
    
    generated = ''.join(result)
    
    # Ici on verifie bien que le nom généré n'existe pas déjà
    # si oui nous reprenons le processus sinon nous retournons le
    # le nom généré
    if generated not in chain['_names']:
        if taille == None :
            return generated
        else:
            if len(generated) == taille:
                return generated
            else:
                print(generated)
                return generate(chain, debut_de_mot, taille)
    else:
        print(generated)
        return generate(chain, debut_de_mot, taille)

def get_communes():
    l = []
    # Récupération du dossier courant
    # Ensuite on joint le chemin du dossier courant 
    # avec le nom du fichier
    my_path = os.getcwd()
    path = os.path.join(my_path, 'communes-01042019.csv')
    with open(path, newline='', encoding='UTF-8') as csvfile:
        spamreader = csv.reader( csvfile, delimiter=',')
        for row in spamreader:
            l.append(row[8])
    l.remove('libelle')
    return l
 
if __name__ == '__main__' :
    # Mise en place d'un marqueur de temps
    _start = datetime.datetime.now()
    
    # --------  main  ---------------
    try:
        liste_des_communes = get_communes()
        markov_chain       = build_markov_chain(liste_des_communes, 3)
        gen                = generate(markov_chain)
    except (FileNotFoundError):
        print("Oops! Le fichier n'a pas été trouvé")
    # --------  main  ---------------
    
    # Marqueur de temps representant la fin du prgramme    
    _end=datetime.datetime.now()
    timecost = ((_end - _start).microseconds/1000)