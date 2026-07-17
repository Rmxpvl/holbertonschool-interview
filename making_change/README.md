
# Projet Making Change

## But du projet

Le but de ce projet est d'implémenter une fonction qui, étant donné une liste de valeurs de pièces et un montant total, détermine le nombre minimal de pièces nécessaires pour atteindre ce montant. On dispose d'un nombre infini de pièces de chaque valeur.

Ce projet évalue la compréhension de la programmation dynamique (bottom-up), la construction d'une table de sous-problèmes, et l'analyse de complexité temporelle et spatiale.

## Exigences fonctionnelles

- Implémenter une fonction `makeChange(coins, total)`.
- `coins` est une liste de valeurs de pièces (entiers strictement positifs).
- On dispose d'un nombre infini de chaque dénomination.
- Si `total` est inférieur ou égal à 0, retourner `0`.
- Si `total` ne peut être atteint avec les pièces données, retourner `-1`.
- Retourner sinon le nombre minimal de pièces nécessaires.
- La performance de la solution est évaluée.

## Idée générale et algorithme

Il s'agit d'un problème classique de programmation dynamique (« coin change », variante minimisation) :

1. Construire une table `fewest` de taille `total + 1`, où `fewest[a]` représente le nombre minimal de pièces pour atteindre le montant `a`.
2. Initialiser `fewest[0] = 0` (montant nul atteint avec 0 pièce) et tous les autres montants à l'infini (non encore atteints).
3. Pour chaque montant `a` de `1` à `total`, essayer chaque pièce `c` :
	- Si `c <= a`, alors `fewest[a] = min(fewest[a], fewest[a - c] + 1)`.
4. À la fin, `fewest[total]` contient la réponse, ou reste à l'infini si `total` est inatteignable (retourner `-1` dans ce cas).

Complexité :
- Temps : O(total * len(coins)), une boucle imbriquée sur les montants et les pièces.
- Espace : O(total), pour la table `fewest`.

## Explication du code fourni

Le fichier principal du projet est `0-making_change.py`. Il contient :

- Une fonction `def makeChange(coins, total):` qui implémente l'algorithme décrit ci-dessus.

Points d'attention dans le code :
- Gérer le cas `total <= 0` en tout début de fonction (retour immédiat de `0`).
- Utiliser `float('inf')` comme valeur « non atteint » plutôt qu'une valeur arbitraire, pour éviter les faux résultats.
- Ne considérer une pièce `c` pour un montant `a` que si `c <= a`, afin de ne pas produire d'indices négatifs.
- Convertir `float('inf')` en `-1` uniquement au retour final, pas pendant le calcul.

## Cas particuliers et exemples

1. Exemple simple :

```
makeChange([1, 2, 25], 37) -> 7
# 25 + 2*6 = 37, soit 1 + 6 = 7 pièces
```

2. Montant inatteignable :

```
makeChange([1256, 54, 48, 16, 102], 1453) -> -1
```

3. Montant nul ou négatif :

```
makeChange([1, 2, 5], 0) -> 0
makeChange([1, 2, 5], -10) -> 0
```

4. Une seule pièce correspond exactement :

```
makeChange([1, 5, 10], 10) -> 1
```

## Comment vérifier et exécuter

```bash
./0-main.py
```

Sortie attendue :

```
7
-1
```

## Conseils pour réussir ce projet

- Dessinez la table `fewest` pour un petit exemple (ex : `coins=[1, 2, 5]`, `total=6`) pour bien visualiser la construction bottom-up.
- Pensez à traiter `total <= 0` avant de construire la table, pour éviter une table de taille négative ou nulle inutile.
- Vérifiez la complexité de votre solution : une approche récursive naïve sans mémoïsation serait bien trop lente pour de grands totaux.

## Débogage fréquent

- Si la fonction retourne toujours `-1`, vérifier que la comparaison `coin <= amount` est correcte et que `fewest[0]` est bien initialisé à `0` (et non à l'infini).
- Si le résultat est trop élevé, vérifier que toutes les pièces sont bien testées pour chaque montant (boucle interne complète sur `coins`).
- Si l'exécution est lente sur de grands totaux, s'assurer que la solution utilise bien une table (bottom-up) et non une récursion sans mémoïsation.
