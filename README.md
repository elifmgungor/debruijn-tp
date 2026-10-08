# Assemblage par graphe de De Bruijn

Implémentation Python réalisée dans le cadre du TP d’assemblage du M2 Bioinformatique, à partir du [projet fourni par Amine Ghozlane](https://github.com/aghozlane/debruijn-tp). L’objectif est de reconstruire le génome de l’entérovirus A71 à partir de lectures simulées, puis de comparer le résultat à la référence.

Le programme lit les séquences FASTQ, compte les k-mers et construit un graphe orienté dont les arêtes sont pondérées par leur fréquence. Il résout les bulles et les pointes d’entrée et de sortie, puis écrit les contigs au format FASTA. Les chemins sont sélectionnés selon leur poids moyen, leur longueur puis, en cas d’égalité, un choix aléatoire avec une graine fixée à 9001.

## Installation

Depuis la racine du dépôt :

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

La comparaison à la référence nécessite aussi BLAST+ (`blastn`).

## Utilisation

```bash
python3 debruijn/debruijn.py -i data/eva71_plus_perfect.fq -k 22 -o contigs.fasta
```

`-i` est obligatoire. La taille des k-mers est de 22 par défaut et le fichier de sortie est `contigs.fasta`. L’option `-f graph.png` permet d’enregistrer une image du graphe final. Les enregistrements FASTQ incomplets ou mal formés produisent une erreur explicite.

Les sous-ensembles demandés dans le TP sont inclus dans `data/` :

```bash
python3 debruijn/debruijn.py -i data/eva71_two_reads.fq -o /tmp/two_reads_contigs.fasta
python3 debruijn/debruijn.py -i data/eva71_hundred_reads.fq -o /tmp/hundred_reads_contigs.fasta
```

## Résultat sur les lectures complètes

Avec `k=22`, l’assemblage produit un contig de **7 391 nucléotides**. BLAST l’aligne sur les positions **12 à 7 402** du génome de référence, long de 7 408 nucléotides, avec **100 % d’identité et aucun gap**. Cela couvre **99,77 %** de la référence ; 11 bases au début et 6 à la fin ne sont pas reconstruites.

Le contig est dans [contigs.fasta](contigs.fasta) et l’alignement détaillé dans [results/eva71_blast.txt](results/eva71_blast.txt). Pour refaire la comparaison sans créer de base BLAST :

```bash
blastn -query contigs.fasta -subject data/eva71.fna -out results/eva71_blast.txt
```

## Vérification

```bash
python3 -m pytest --cov=debruijn -v -s
python3 -m pylint debruijn/debruijn.py
```

Les tests du TP vérifient la lecture FASTQ, les k-mers, la construction du graphe, les contigs et la simplification des bulles et des pointes. Des tests supplémentaires couvrent les FASTQ mal formés. Les signatures des fonctions imposées sont conservées.

## Données et limites

`data/eva71.fna` contient la référence EVA71 et `data/eva71_plus_perfect.fq` les lectures simulées fournies pour le TP. Les fichiers à deux et cent lectures sont des extraits de ce FASTQ. Ces lectures ont été générées avec ART, sans insertion ni erreur, uniquement dans le sens 5’ → 3’.

Cette implémentation suit les simplifications du TP : elle recherche des chemins simples entre entrées et sorties et ne vise pas un assembleur général pour des génomes complexes ou circulaires. Le résultat sur ces lectures simulées ne mesure pas sa robustesse sur des données réelles.

## Source du TP

[Énoncé](https://docs.google.com/document/d/1P4v3bHbSurD7RXA-ldVwmtNKGvWsnBae51RMGye_KLs/edit?usp=sharing) · [Dépôt de départ](https://github.com/aghozlane/debruijn-tp)

Le code conserve les mentions de licence GPL du projet de départ.
