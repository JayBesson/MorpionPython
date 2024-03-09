from collections import Counter
# ^ Importation du module Counter pour compter les occurrences dans la grille

VIDE = 0
JOUEUR_X = 1
JOUEUR_O = -1
# ^ Définition des constantes pour les valeurs dans la grille

# v Fonction pour déterminer le joueur actuel en fonction de la grille
def joueur(grille):
    # Utilisation de Counter pour compter le nombre d'occurrences de chaque joueur

    compteur = Counter(grille)
    places_X = compteur[1]
    places_O = compteur[-1]
    # Logique pour déterminer le joueur actuel

    if places_X + places_O == 9:
        return None
    elif places_X > places_O:
        return JOUEUR_O
    else:
        return JOUEUR_X
    
# v Fonction pour obtenir les actions possibles dans la grille
def actions(grille):
    play = joueur(grille)
    # Création d'une liste d'actions possibles sous forme de tuples (joueur, index)
    liste_actions = [(play, i) for i in range(len(grille)) if grille[i] == VIDE]
    return liste_actions

# v Fonction pour obtenir la grille après une action donnée

def resultat(grille, action):
    (play, index) = action
    grille_copie = grille.copy()
    grille_copie[index] = play
    return grille_copie

# v Fonction pour déterminer si la partie est terminée et qui a gagné

def terminal(grille):
    for i in range(3):
        if grille[3 * i] == grille[3 * i + 1] == grille[3 * i + 2] != VIDE:
            return grille[3 * i]
        if grille[i] == grille[i + 3] == grille[i + 6] != VIDE:
            return grille[i]

    if grille[0] == grille[4] == grille[8] != VIDE:
        return grille[0]
    if grille[2] == grille[4] == grille[6] != VIDE:
        return grille[2]

    if joueur(grille) is None:
        return 0
    
    return None

# v Fonction récursive pour évaluer l'utilité d'une grille donnée

def utilite(grille, cout):
    term = terminal(grille)
    if term is not None:
        return (term, cout)
    
    liste_actions = actions(grille)
    utils = []
    for action in liste_actions:
        nouvelle_grille = resultat(grille, action)
        utils.append(utilite(nouvelle_grille, cout + 1))

    score = utils[0][0]
    idx_cout = utils[0][1]
    play = joueur(grille)
    if play == JOUEUR_X:
        for i in range(len(utils)):
            if utils[i][0] > score:
                score = utils[i][0]
                idx_cout = utils[i][1]
    else:
        for i in range(len(utils)):
            if utils[i][0] < score:
                score = utils[i][0]
                idx_cout = utils[i][1]
    return (score, idx_cout) 

# v Fonction utilisant l'algorithme minimax pour déterminer la meilleure action

def minimax(grille):
    liste_actions = actions(grille)
    utils = []
    for action in liste_actions:
        nouvelle_grille = resultat(grille, action)
        utils.append((action, utilite(nouvelle_grille, 1)))

    if len(utils) == 0:
        return ((0, 0), (0, 0))

    liste_triee = sorted(utils, key=lambda l: l[0][1])
    action = min(liste_triee, key=lambda l: l[1])
    return action

# v Fonction pour afficher la grille de manière conviviale

def afficher_grille(grille):
    def convertir(num):
        if num == JOUEUR_X:
            return '❌'
        if num == JOUEUR_O:
            return '⭕️'
        return '_'

    i = 0
    for _ in range(3):
        for _ in range(3):
            print(convertir(grille[i]), end=' ')
            i += 1
        print()

if __name__ == '__main__':
    
    # Boucle principale pour permettre aux joueurs de jouer plusieurs parties

    while True:
        grille_jeu = [VIDE for _ in range(9)]
        print('|------- BIENVENUE DANS LE SUPER MORPION -----------|')
        print('Vous êtes ❌ tandis que votre adversaire est ⭕️')

        while terminal(grille_jeu) is None:
            jouer = joueur(grille_jeu)
            if jouer == JOUEUR_X:
                print('\n\nC\'est à votre tour', end='\n\n')

                while True:
                    try:
                        horizontale = int(input('Saisissez la coordonnée horizontale [1-3] : '))
                        verticale = int(input('Saisissez la coordonnée verticale [1-3] : '))
                        index = 3 * (horizontale - 1) + (verticale - 1)

                        if not (1 <= horizontale <= 3) or not (1 <= verticale <= 3) or not grille_jeu[index] == VIDE:
                            raise ValueError("Coordonnées invalides. Veuillez réessayer.")
                        
                        grille_jeu = resultat(grille_jeu, (1, index))
                        afficher_grille(grille_jeu)
                        break

                    except ValueError as e:
                        print(e)
            else:
                print('\n\nL\'ordinateur joue son tour')
                action = minimax(grille_jeu)
                grille_jeu = resultat(grille_jeu, action[0])
                afficher_grille(grille_jeu)

        gagnant = utilite(grille_jeu, 1)[0]
        if gagnant == JOUEUR_X:
            print("Vous avez gagné !")
        elif gagnant == JOUEUR_O:
            print("Vous avez perdu !")
        else:
            print("C'est une égalité.")

        # Proposer de rejouer
            
        rejouer = input("Voulez-vous rejouer ? (oui/non): ").lower()
        if rejouer != "oui":
            break
