
# Projet Prime Game

## But du projet

Le but de ce projet est d'implémenter une fonction qui détermine le gagnant d'un jeu joué par Maria et Ben sur plusieurs manches. Pour chaque manche, on part de l'ensemble des entiers consécutifs de `1` à `n`. À tour de rôle (Maria commence), chaque joueur choisit un nombre premier encore présent dans l'ensemble et retire ce nombre ainsi que tous ses multiples. Le joueur qui ne peut plus jouer perd la manche. En jouant `x` manches (avec un `n` potentiellement différent à chaque fois), on doit déterminer quel joueur a gagné le plus de manches.

Ce projet évalue la capacité à repérer un invariant mathématique caché derrière un jeu combinatoire, plutôt que de simuler le jeu coup par coup, ainsi que la construction d'un crible de nombres premiers efficace (Sieve of Eratosthenes) pour respecter les contraintes de performance.

## Exigences fonctionnelles

- Implémenter une fonction `isWinner(x, nums)`.
- `x` est le nombre de manches jouées, `nums` est la liste des valeurs de `n` pour chaque manche.
- Maria joue toujours en premier ; les deux joueurs jouent de façon optimale.
- Retourner le nom du joueur ("Maria" ou "Ben") qui a gagné le plus de manches.
- Si le nombre de victoires est égal entre les deux joueurs (gagnant indéterminable), retourner `None`.
- `n` et `x` ne dépasseront pas `10000`.
- Aucun import de package n'est autorisé dans ce fichier.
- La performance de la solution est évaluée.

## Idée générale et algorithme

Simuler le jeu manche par manche serait trop coûteux pour de grandes valeurs de `n`. La clé est une observation mathématique : **le résultat d'une manche ne dépend que de la parité du nombre de nombres premiers inférieurs ou égaux à `n`.**

- Choisir un nombre premier `p` élimine `p` et tous ses multiples, ce qui revient toujours à retirer un nombre premier « disponible » de l'ensemble (les multiples non premiers ne peuvent de toute façon plus être choisis directement). Le jeu se réduit donc à retirer, tour à tour, un élément parmi les nombres premiers ≤ `n`.
- Si le nombre de nombres premiers ≤ `n` est **impair**, Maria (qui commence) fait le dernier choix possible et gagne.
- Si ce nombre est **pair**, c'est Ben qui fait le dernier choix et gagne.

Algorithme :

1. Calculer `max_n`, le plus grand `n` parmi `nums`.
2. Construire un crible d'Ératosthène jusqu'à `max_n` pour marquer les nombres premiers.
3. Construire un tableau de préfixes `primes_up_to`, où `primes_up_to[i]` est le nombre de nombres premiers ≤ `i`.
4. Pour chaque `n` de `nums`, regarder la parité de `primes_up_to[n]` :
	- Impair → victoire de Maria.
	- Pair → victoire de Ben.
5. Comparer le nombre total de victoires de chaque joueur et retourner le nom du vainqueur, ou `None` en cas d'égalité.

Complexité :
- Temps : O(max_n log(log(max_n))) pour le crible, puis O(max_n) pour les préfixes et O(x) pour évaluer chaque manche.
- Espace : O(max_n) pour le crible et le tableau de préfixes.

## Explication du code fourni

Le fichier principal du projet est `0-prime_game.py`. Il contient :

- Une fonction `def isWinner(x, nums):` qui implémente l'algorithme décrit ci-dessus (crible + parité + comptage des victoires).

Points d'attention dans le code :
- Gérer le cas `nums` vide ou `x == 0` en retournant immédiatement `None`.
- Marquer `0` et `1` comme non premiers avant de lancer le crible.
- Ne cribler qu'à partir de `i * i` (optimisation standard du crible d'Ératosthène).
- Utiliser un tableau de préfixes pour obtenir le nombre de premiers ≤ `n` en O(1) par manche, plutôt que de recompter à chaque fois.
- Ne pas utiliser `import` (contrainte de l'énoncé) : `int(max_n ** 0.5)` remplace `math.sqrt` sans import.

## Cas particuliers et exemples

1. Exemple de l'énoncé :

```
x = 3, nums = [4, 5, 1]
isWinner(3, [4, 5, 1]) -> "Ben"
# n=4 -> 2 premiers (pair) -> Ben
# n=5 -> 3 premiers (impair) -> Maria
# n=1 -> 0 premier (pair) -> Ben
# Ben: 2 victoires, Maria: 1 victoire -> Ben gagne
```

2. Exemple du fichier de test :

```
isWinner(5, [2, 5, 1, 4, 3]) -> "Ben"
```

3. Égalité (résultat indéterminable) :

```
isWinner(2, [4, 5]) -> None
# n=4 -> Ben, n=5 -> Maria -> égalité 1-1
```

4. Liste vide ou aucune manche :

```
isWinner(0, []) -> None
```

## Comment vérifier et exécuter

```bash
./main_0.py
```

Sortie attendue :

```
Winner: Ben
```

## Conseils pour réussir ce projet

- Ne cherchez pas à simuler le jeu tour par tour : concentrez-vous sur la parité du nombre de nombres premiers ≤ `n`, c'est la clé de la solution efficace.
- Construisez le crible une seule fois jusqu'au maximum de `nums`, puis réutilisez-le pour toutes les manches au lieu de le reconstruire à chaque fois.
- Vérifiez vos résultats à la main sur les petits exemples de l'énoncé (`n=4`, `n=5`, `n=1`) avant de généraliser.

## Débogage fréquent

- Si les résultats sont inversés (Maria/Ben échangés), vérifier le sens de la parité : impair -> Maria, pair -> Ben.
- Si le crible est incorrect, s'assurer que `0` et `1` sont bien exclus des nombres premiers avant de cribler.
- Si la fonction est trop lente sur de grandes entrées, vérifier qu'un seul crible est construit jusqu'à `max(nums)`, plutôt qu'un crible recalculé pour chaque valeur de `nums`.
