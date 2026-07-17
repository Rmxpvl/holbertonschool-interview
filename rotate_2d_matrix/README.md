
# Projet Rotate 2D Matrix

## But du projet

Le but de ce projet est d'implémenter une fonction qui fait pivoter une matrice carrée `n x n` de 90 degrés dans le sens horaire, **en place** (sans allouer de nouvelle matrice ni retourner de valeur).

Ce projet évalue la compréhension de la manipulation de tableaux 2D, la capacité à raisonner sur les indices lors de transformations géométriques, et la gestion de la mutation en place (sans structure auxiliaire).

## Exigences fonctionnelles

- Implémenter une fonction `rotate_2d_matrix(matrix)`.
- La matrice est carrée (`n x n`), à deux dimensions, et non vide.
- La fonction ne doit rien retourner : elle doit modifier `matrix` directement.

## Idée générale et algorithme

Faire pivoter une matrice de 90° dans le sens horaire revient à :

1. **Transposer** la matrice (échanger `matrix[i][j]` et `matrix[j][i]` pour toutes les paires au-dessus de la diagonale).
2. **Inverser chaque ligne** de la matrice transposée.

Algorithme :

- Pour `i` de `0` à `n - 1` :
	- Pour `j` de `i + 1` à `n - 1` :
		- Échanger `matrix[i][j]` et `matrix[j][i]`.
- Pour chaque ligne de `matrix` :
	- Inverser la ligne (`reverse()`).

Complexité :
- Temps : O(n²), chaque élément est visité un nombre constant de fois.
- Espace : O(1), la rotation se fait en place (hors matrice d'entrée).

## Explication du code fourni

Le fichier principal du projet est `0-rotate_2d_matrix.py`. Il contient :

- Une fonction `def rotate_2d_matrix(matrix):` qui implémente l'algorithme décrit ci-dessus (transposition puis inversion des lignes).

Points d'attention dans le code :
- Ne parcourir que la moitié supérieure de la matrice lors de la transposition (`j` commence à `i + 1`) pour ne pas annuler l'échange en repassant sur la même paire.
- Utiliser l'affectation multiple de Python (`a, b = b, a`) pour échanger les valeurs sans variable temporaire.
- Modifier `matrix` en place : ne pas créer et retourner une nouvelle matrice.

## Cas particuliers et exemples

1. Exemple simple (3x3) :

```
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

rotate_2d_matrix(matrix)
# matrix == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
```

2. Matrice 1x1 (inchangée) :

```
matrix = [[42]]
rotate_2d_matrix(matrix)
# matrix == [[42]]
```

3. Matrice 2x2 :

```
matrix = [[1, 2],
          [3, 4]]

rotate_2d_matrix(matrix)
# matrix == [[3, 1], [4, 2]]
```

## Comment vérifier et exécuter

```bash
./main_0.py
```

Sortie attendue :

```
[[7, 4, 1], [8, 5, 2], [9, 6, 3]]
```

## Conseils pour réussir ce projet

- Faites le calcul à la main sur une matrice 3x3 pour bien visualiser la transposition puis l'inversion des lignes.
- Vérifiez que la boucle de transposition ne parcourt bien que la moitié de la matrice (`j > i`), sinon les échanges s'annulent.
- Testez avec des matrices de tailles différentes (1x1, 2x2, impaire, paire) pour confirmer que l'algorithme généralise correctement.

## Débogage fréquent

- Si la matrice revient à son état d'origine après rotation, la boucle de transposition parcourt probablement toute la matrice au lieu de sa moitié supérieure.
- Si le résultat est une rotation dans le mauvais sens (anti-horaire), vérifier l'ordre des opérations : transposition **puis** inversion des lignes (et non l'inverse).
