# Log Parsing

## Objectif de l'exercice

Écrire un script Python qui lit des logs depuis l'**entrée standard**, ligne
par ligne, puis calcule des statistiques sur les lignes valides.

Le script doit afficher régulièrement :

- la taille totale des fichiers traités,
- le nombre d'occurrences de certains codes de statut HTTP.

Il doit aussi **ignorer** les lignes qui ne respectent pas le format
attendu, et produire un résumé toutes les 10 lignes, ainsi qu'au moment
d'une interruption clavier (`Ctrl+C`).

---

## Sommaire

1. [Lire l'entrée standard ligne par ligne](#1-lire-lentrée-standard-ligne-par-ligne)
2. [Le format de log et les expressions régulières](#2-le-format-de-log-et-les-expressions-régulières)
3. [Accumuler des statistiques](#3-accumuler-des-statistiques)
4. [Afficher un résumé périodique](#4-afficher-un-résumé-périodique)
5. [Gérer l'interruption clavier (`Ctrl+C`)](#5-gérer-linterruption-clavier-ctrlc)
6. [Lecture pas à pas du script complet](#6-lecture-pas-à-pas-du-script-complet)
7. [Tester le script](#7-tester-le-script)
8. [Pièges fréquents](#8-pièges-fréquents)
9. [Pour aller plus loin](#9-pour-aller-plus-loin)

---

## 1. Lire l'entrée standard ligne par ligne

```python
import sys

for raw_line in sys.stdin:
    ...
```

- `sys.stdin` est un objet "fichier" représentant l'**entrée standard** : ce
  que le programme reçoit via un **pipe** (`|`) ou une redirection (`<`).
- `for line in sys.stdin:` lit **une ligne à la fois**, indéfiniment, jusqu'à
  ce que l'entrée se termine (`EOF`, *End Of File*) ou qu'une interruption
  survienne.
- Cette approche est **streaming** : le script n'a jamais besoin de charger
  tout le fichier en mémoire, ce qui est crucial pour des logs de plusieurs
  gigaoctets.

Exemple d'utilisation typique :

```bash
generate_logs.py | python3 0-stats.py
```

Le programme `generate_logs.py` produit des lignes en continu, qui sont
envoyées directement (via le `|`) sur l'entrée standard de `0-stats.py`.

---

## 2. Le format de log et les expressions régulières

Une ligne de log valide ressemble à :

```
192.168.0.1 - [2024-01-01 12:00:00] "GET /projects/260 HTTP/1.1" 200 1024
```

Pour extraire le **code de statut** (`200`) et la **taille** (`1024`), on
utilise une **expression régulière** (module `re`) :

```python
import re

pattern = re.compile(
    r'^\S+ - \[[^\]]+\] "GET /projects/\S+ HTTP/1\.1"\s+(\d+)\s+(\d+)'
)
```

Décomposition du motif :

| Morceau | Signification |
|---------|----------------|
| `^\S+` | Début de ligne, suivi d'une suite de caractères non-espaces (l'IP) |
| ` - ` | Texte littéral exact |
| `\[[^\]]+\]` | Une date entre crochets : `[...]` où `...` ne contient pas de `]` |
| `"GET /projects/\S+ HTTP/1\.1"` | La requête HTTP, entre guillemets (le `.` doit être échappé : `\.`) |
| `\s+(\d+)` | Un ou plusieurs espaces, puis **un groupe capturant** une suite de chiffres → le **code de statut** |
| `\s+(\d+)` | Idem → la **taille** du fichier |

- `re.compile(pattern)` **précompile** l'expression régulière une seule fois
  (en dehors de la boucle), ce qui est beaucoup plus performant que de la
  recompiler à chaque ligne.
- `pattern.search(line)` cherche le motif **n'importe où** dans la chaîne et
  retourne un objet `Match` si trouvé, sinon `None`.
- `match.group(1)` et `match.group(2)` récupèrent le contenu des deux
  **groupes capturants** `(\d+)`, c'est-à-dire le code de statut et la
  taille — toujours sous forme de **chaînes**, à convertir avec `int(...)`.

### Pourquoi `if match:` ?

Si la ligne ne correspond pas exactement au format attendu (ligne corrompue,
vide, ou différente), `pattern.search()` retourne `None`. Le test
`if match:` permet d'**ignorer silencieusement** ces lignes invalides sans
faire planter le script.

---

## 3. Accumuler des statistiques

```python
status_codes = [200, 301, 400, 401, 403, 404, 405, 500]
counts = {code: 0 for code in status_codes}
file_size = 0
line_count = 0
```

- `counts = {code: 0 for code in status_codes}` est une **compréhension de
  dictionnaire** : elle construit
  `{200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}` en une
  seule ligne, équivalent à :

  ```python
  counts = {}
  for code in status_codes:
      counts[code] = 0
  ```

- À chaque ligne valide :

  ```python
  status = int(match.group(1))
  size = int(match.group(2))
  file_size += size
  if status in counts:
      counts[status] += 1
  ```

  - `file_size` accumule la taille **de toutes** les lignes valides, quel
    que soit le code de statut.
  - `counts[status] += 1` n'incrémente que si le code fait partie de la
    liste surveillée (`if status in counts:`) — un code `204` par exemple
    serait ignoré pour le comptage, mais sa taille compterait toujours dans
    `file_size`.

---

## 4. Afficher un résumé périodique

```python
def print_stats():
    print("File size: {}".format(file_size))
    for code in status_codes:
        if counts[code]:
            print("{}: {}".format(code, counts[code]))
```

- On affiche la taille totale, puis **uniquement les codes dont le compteur
  est non nul** (`if counts[code]:` — `0` est "faux" en Python).
- L'ordre d'affichage suit `status_codes`, donc toujours **trié** (200, 301,
  400...), même si les lignes sont arrivées dans le désordre.
- Cette fonction est appelée à plusieurs endroits (toutes les 10 lignes, à la
  fin, et lors d'une interruption) : **factoriser l'affichage dans une
  fonction évite la duplication de code**.

Déclenchement périodique :

```python
if line_count % 10 == 0:
    print_stats()
```

`%` est l'opérateur **modulo** (reste de la division). `line_count % 10 == 0`
est vrai pour `line_count` valant `10, 20, 30...` — donc le résumé s'affiche
toutes les 10 lignes traitées, qu'elles soient valides ou non.

---

## 5. Gérer l'interruption clavier (`Ctrl+C`)

```python
try:
    for raw_line in sys.stdin:
        ...
    if line_count == 0 or line_count % 10 != 0:
        print_stats()
except KeyboardInterrupt:
    print_stats()
    raise
```

- Appuyer sur `Ctrl+C` envoie le **signal** `SIGINT` au programme, que Python
  transforme en exception `KeyboardInterrupt`.
- En l'attrapant, le script peut **afficher un dernier résumé** avant de
  s'arrêter, même si on est en plein milieu d'un groupe de 10 lignes.
- `raise` (sans argument) **relance** l'exception déjà attrapée : le script
  affiche bien les statistiques, mais se termine quand même comme prévu suite
  à l'interruption (code de sortie non nul), sans masquer l'événement.
- Après la boucle (si elle se termine normalement, par `EOF`), on affiche un
  dernier résumé **seulement si** il reste des lignes non comptabilisées
  depuis le dernier multiple de 10 (`line_count % 10 != 0`), ou si aucune
  ligne n'a été lue (`line_count == 0`, pour afficher au moins
  `File size: 0`).

---

## 6. Lecture pas à pas du script complet

```python
#!/usr/bin/python3
import sys
import re

status_codes = [200, 301, 400, 401, 403, 404, 405, 500]
counts = {code: 0 for code in status_codes}
file_size = 0
line_count = 0
pattern = re.compile(
    r'^\S+ - \[[^\]]+\] "GET /projects/\S+ HTTP/1\.1"\s+(\d+)\s+(\d+)'
)


def print_stats():
    print("File size: {}".format(file_size))
    for code in status_codes:
        if counts[code]:
            print("{}: {}".format(code, counts[code]))


if __name__ == "__main__":
    try:
        for raw_line in sys.stdin:
            line_count += 1
            match = pattern.search(raw_line.rstrip("\n"))
            if match:
                status = int(match.group(1))
                size = int(match.group(2))
                file_size += size
                if status in counts:
                    counts[status] += 1
            if line_count % 10 == 0:
                print_stats()
        if line_count == 0 or line_count % 10 != 0:
            print_stats()
    except KeyboardInterrupt:
        print_stats()
        raise
```

Diagramme du flux d'exécution :

```
sys.stdin (flux de lignes)
        │
        ▼
  pour chaque ligne :
        │
        ├─ line_count += 1
        ├─ pattern.search(ligne) ─── pas de match ──► ligne ignorée
        │         │ match
        │         ▼
        │   extraire status, size
        │   file_size += size
        │   counts[status] += 1 (si surveillé)
        │
        └─ line_count % 10 == 0 ? ── oui ──► print_stats()
        │
   (EOF ou Ctrl+C)
        │
        ▼
  print_stats() final
```

---

## 7. Tester le script

```bash
# Lecture depuis un fichier de logs existant
cat access.log | python3 0-stats.py

# Lecture depuis un générateur de logs aléatoires
python3 generate_logs.py | python3 0-stats.py

# Arrêt manuel pour vérifier le résumé final
python3 generate_logs.py | python3 0-stats.py
# (puis Ctrl+C)
```

---

## 8. Pièges fréquents

| Erreur | Conséquence | Solution |
|--------|-------------|----------|
| Recompiler le `pattern` à chaque ligne (`re.search(motif, ligne)` dans la boucle) | Performances dégradées sur de gros volumes | `re.compile(...)` **une seule fois**, en dehors de la boucle |
| Oublier `if match:` | `AttributeError: 'NoneType' object has no attribute 'group'` sur une ligne invalide | Toujours vérifier que `match` n'est pas `None` avant `.group(...)` |
| Incrémenter `counts[status]` sans vérifier `status in counts` | `KeyError` si un code non prévu apparaît | Toujours tester l'appartenance avant d'indexer un dict avec une clé externe |
| Oublier le résumé final après la boucle | Les dernières lignes (moins de 10) ne sont jamais affichées | Appeler `print_stats()` après la boucle si nécessaire |
| Laisser `KeyboardInterrupt` se propager sans l'attraper | Le script s'arrête brutalement sans résumé | `try/except KeyboardInterrupt:` + `print_stats()` avant `raise` |
| Convertir `match.group(1)` en `int` sans s'assurer que c'est bien numérique | `ValueError` | Le motif `(\d+)` garantit déjà qu'il s'agit de chiffres, donc `int()` est sûr **si le match a réussi** |

---

## 9. Pour aller plus loin

- **`re.match` vs `re.search`** : `match` n'essaie qu'au **début** de la
  chaîne, `search` cherche **partout**. Ici, `^` dans le motif rend les deux
  équivalents.
- **Modules de logs structurés** (`logging`, formats JSON) : évitent d'avoir
  à parser du texte avec des regex, au prix d'un format moins lisible
  "à l'œil".
- **`collections.Counter`** : alternative au dictionnaire manuel pour compter
  des occurrences.
- Ce script illustre un pattern très courant en traitement de données :
  **lire un flux en continu, accumuler un état, produire des rapports
  périodiques** — la base de nombreux outils de monitoring.
