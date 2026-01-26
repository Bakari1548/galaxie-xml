# Galaxie XML - Cas pratiques

Ce dépôt contient des cas pratiques pour la manipulation de données XML avec la Galaxie XML 

Les exemples incluent la modélisation d'une assemblée nationale avec des députés, des commissions, des sessions et des lois.

## Structure de assemblee_nationale.xml
Le fichier `assemblee_nationale.xml` est structuré selon la DTD définie dans `assemblee_nationale.dtd`. Il comprend les éléments suivants :
- `<assemblee_nationale>` : Élément racine contenant toutes les données de l'assemblée.
- `<informations_generales>` : Contient les informations générales sur l'assemblée nationale.
- `<deputes>` : Contient les informations sur les députés.
- `<lois>` : Contient les informations sur les lois proposées et adoptées.
- `<commissions>` : Contient les informations sur les commissions parlementaires.
- `<sessions>` : Contient les informations sur les sessions parlementaires.

