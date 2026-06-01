# Kayak_Jedha
Kayak plan your trip - Bloc 1 Data Collection &amp; Management Jedha project

## 🎯 Contexte & Objectif Métier
Le département marketing de **Kayak** a mis en évidence que 70% des utilisateurs planifiant un voyage réclament des informations fiables et centralisées sur leurs destinations. 
Pour répondre à ce besoin, ce projet déploie une application d'ingénierie de données capable de collecter, stocker et structurer en temps réel des données combinées sur la **météo à 7 jours** et la **satisfaction des structures hôtelières** afin de recommander dynamiquement le Top-5 des destinations idéales en France ainsi que leurs 20 meilleurs hôtels.

---

## 🏗️ Architecture du Pipeline de Données (Data Infrastructure)

Le projet s'articule autour d'une architecture Cloud moderne et étanche respectant le flux de données suivant :

1. **Ingestion & Extraction (Acquisition) :**
   * **Données Géographiques :** Requêtage de l'API `Nominatim` pour convertir les 35 villes du scope en coordonnées GPS (Lat/Lon) avec un protocole strict de politesse réseau (`rate-limiting`).
   * **Données Météorologiques :** Extraction des prévisions sur 7 jours via l'API `OpenWeatherMap (One Call API)`. Calcul d'un indicateur métier exclusif (*Weather Score*) pondérant les températures journalières et pénalisant les précipitations.
   * **Web-Scraping Hôtelier :** Utilisation de `Playwright` en mode asynchrone/headless avec stratégies d'atténuation anti-bot pour moissonner le catalogue d'hôtels sur `Booking.com`.

2. **Stockage de Masse (Data Lake) :**
   * Centralisation des fichiers plats consolidés et horodatés au format `.csv` au sein d'un bucket sécurisé **AWS S3** faisant office de source unique de vérité (*Raw Data Layer*).

3. **Data Warehouse (Stockage Relationnel) :**
   * Conception et déploiement d'une base de données relationnelle managée via **AWS RDS (PostgreSQL)**. 
   * Phase d'**ETL** exécutée via `SQLAlchemy` pour charger les structures de données nettoyées et mise en place de vues analytiques (`v_cities_hotels_enriched`) pour optimiser les performances de requêtage des analystes BI.

---

## 🚀 Réalisation des Livrables Graphiques

Conformément aux exigences strictes du cahier des charges, deux livrables cartographiques ont été générés à l'aide de la bibliothèque Plotly (sauvegardés aux formats interactifs HTML et statiques PNG dans le répertoire `outputs/viz/`) :

* **📌 Carte 1 : Top-5 des Destinations Françaises** — Cartographie dynamique isolant les 5 villes affichant le meilleur score météorologique agrégé sur 7 jours.
* **🏨 Carte 2 : Top-20 des Hôtels Partenaires** — Visualisation géospatiale des 20 établissements affichant les meilleures notes d'évaluation au sein de ces zones d'intérêt.

---

## 📂 Structure du Répertoire GitHub

```text
📦 kayak_Jedha
 ┣ 📂 notebook
 ┃ ┗ 📜 2.projet_kayak_AMK.ipynb      # Pipeline ETL complet, connexion RDS et requêtes analytiques
 ┣ 📂 script
 ┃ ┗ 📜 scrape_booking.py             # Script de scraping Playwright (Booking.com)
 ┣ 📂 outputs
 ┃ ┗ 📂 maps
 ┃   ┣ 📜 top_5_destinations_map.html # Carte interactive des villes (HTML)
 ┃   ┣ 📜 top_5_destinations_map.png  # Capture statique des villes pour présentation
 ┃   ┣ 📜 top_20_hotels_map.html      # Carte interactive des hôtels (HTML)
 ┃   ┗ 📜 top_20_hotels_map.png       # Capture statique des hôtels pour présentation
 ┃ ┗ 📂 data
 ┃   ┣ 📜 cities_hotels_enriched.csv   # Dataset final consolidé (Météo + Hôtels) importé dans le Data Warehouse RDS
 ┃   ┣ 📜 city_scores_20january2026.csv  # Résultats bruts de l'API OpenWeather avec calcul du Weather Score par ville
 ┃   ┣ 📜 hotels_top5.csv              # Données brutes extraites de Booking.com via le script de scraping Playwright
 ┃   ┗ 📜 hotels_top5_clean.csv        # Données hôtelières nettoyées et typées (parsing des scores d'évaluation)
 ┗ 📜 README.md                       # Documentation officielle du projet

👨‍💻 Auteur
Projet conçu, architecturé et codé par Alicia Marzouk dans le cadre du Bloc 1 — Data Collection & Management, certification CDSD RNCP35288 - Niveau 6, Jedha Bootcamp.
