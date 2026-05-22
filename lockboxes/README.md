
# Projet Lockboxes

## But du projet

Le but de ce projet est d'implémenter une fonction qui détermine si l'on peut ouvrir toutes les boîtes (lockboxes) en partant de la boîte 0. Chaque boîte contient une liste de clés, chaque clé est un entier représentant le numéro d'une boîte. On ne peut ouvrir une boîte que si l'on possède sa clé. On commence avec la boîte 0 ouverte et on utilise les clés trouvées pour ouvrir d'autres boîtes.

Ce projet évalue la compréhension des parcours de graphe (BFS/DFS), la gestion des structures de données (listes, piles/queues), et l'analyse de complexité temporelle et spatiale.

## Exigences fonctionnelles

- Implémenter une fonction `canUnlockAll(boxes)` (ou équivalent) qui prend en entrée une liste de listes `boxes` où `boxes[i]` contient les clés trouvées dans la boîte `i`.
- La fonction doit retourner `True` si toutes les boîtes peuvent être ouvertes, `False` sinon.
- Commencer avec la boîte `0` ouverte.

## Idée générale et algorithme

1. Traiter le problème comme un graphe dirigé où chaque boîte est un nœud et une clé vers la boîte `j` est une arête dirigée vers `j`.
2. Partir de la boîte `0` et effectuer un parcours en profondeur (DFS) ou en largeur (BFS) pour visiter toutes les boîtes accessibles.
3. Garder un ensemble/list des boîtes déjà ouvertes pour éviter les répétitions.
4. Après le parcours, vérifier si le nombre de boîtes ouvertes est égal au nombre total de boîtes.

Algorithme (DFS itératif avec pile) :

- Initialiser une pile avec la boîte `0`.
- Initialiser un ensemble `opened = {0}`.
- Tant que la pile n'est pas vide :
	- Pop une boîte `curr` de la pile.
	- Pour chaque clé `k` dans `boxes[curr]` :
		- Si `k` est dans l'intervalle valide (0 <= k < len(boxes)) et `k` n'est pas dans `opened` :
			- Ajouter `k` à `opened` et empiler `k`.
- Retourner `len(opened) == len(boxes)`.

Complexité :
- Temps : O(N + E) où N est le nombre de boîtes et E le nombre total de clés (itérations au plus une fois par clé).
- Espace : O(N) pour l'ensemble `opened` et la pile/queue.

## Explication du code fourni

Le fichier principal du projet est `0-lockboxes.py` (ou `0-lockboxes.py` selon le dépôt). Le script contient généralement :

- Une fonction principale `def canUnlockAll(boxes):` qui implémente l'algorithme décrit ci-dessus.
- Un bloc `if __name__ == "__main__":` avec des cas de test ou des assertions pour valider le comportement.

Points d'attention dans le code :
- Valider que les clés sont dans l'intervalle correct avant de tenter d'ouvrir une boîte (ignorer les clés invalides).
- Éviter d'empiler plusieurs fois la même boîte en vérifiant l'ensemble `opened` avant d'ajouter.
- Gérer les cas particuliers : liste vide, boîte sans clés, clés répétées, clés pointant vers la même boîte.

## Cas particuliers et exemples

1. Exemple simple (toutes ouvertes) :

```
boxes = [[1], [2], [3], []]
canUnlockAll(boxes) -> True
```

2. Exemple impossible :

```
boxes = [[1, 3], [3, 0, 1], [2], [0]]
canUnlockAll(boxes) -> False  # la boîte 2 est isolée
```

3. Cas avec clés invalides :

```
boxes = [[10], [], []]
canUnlockAll(boxes) -> False  # clé 10 ignorée, seules boîtes 0 ouvertes
```

4. Cas minimal :

```
boxes = []
canUnlockAll(boxes) -> True  # aucune boîte à ouvrir
```

## Comment vérifier et exécuter

- Pour tester localement, exécuter `python3 0-lockboxes.py` (ou le nom exact du fichier) si des tests sont inclus.
- Écrire des assertions ou des tests unitaires pour couvrir les cas ci-dessus.
- Exemple de test rapide dans un shell :

```bash
python3 -c "from 0-lockboxes import canUnlockAll; print(canUnlockAll([[1],[2],[3],[]]))"
```

Remarque : adaptez le nom du module si le fichier s'appelle différemment.

## Conseils pour réussir ce projet

- Commencez par écrire des tests simples et vérifiez votre fonction sur eux.
- Dessinez l'état des boîtes et des clés pour des exemples de petite taille pour comprendre le flux.
- Utilisez un parcours itératif pour éviter les limites de récursion si le nombre de boîtes est grand.
- Vérifiez toutes les entrées (clés hors plage, types inattendus) si les tests le demandent.
- Documentez votre code clairement : nommez la fonction `canUnlockAll`, commentez les étapes clés.

## Débogage fréquent

- Si des boîtes restent inaccessibles, afficher l'ensemble `opened` et la pile à chaque itération pour voir pourquoi certaines clés ne sont pas explorées.
- S'assurer que `opened` reçoit bien la boîte `0` au départ.
- Si vous utilisez recursion, vérifiez la profondeur maximale pour les grands inputs.

---

Si vous voulez, je peux :
- Ouvrir et commenter le fichier `0-lockboxes.py` directement.
- Ajouter des tests unitaires dans un fichier `tests.py`.
- Exécuter quelques tests pour valider l'implémentation.

