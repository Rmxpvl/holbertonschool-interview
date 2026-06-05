# Log Parsing

## Objectif de l'exercice

Écrire un script Python qui lit les logs depuis l'entrée standard, ligne par ligne, puis calcule des statistiques sur les lignes valides.

Le script doit afficher régulièrement :

- la taille totale des fichiers traités
- le nombre d'occurrences pour certains codes de statut HTTP

Il doit aussi ignorer les lignes qui ne respectent pas le format attendu et produire un résumé toutes les 10 lignes, ainsi qu'au moment d'une interruption clavier.
