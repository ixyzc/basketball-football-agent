# NBA 🏀 & Football ⚽ Agent

Pour les nouveaux férus de football ou de basketball, l'année 2024-2025 a su jusque-là offrir un divertissement plein de surprises de rebondissements :

- Le PSG qualifié en finale de Ligue des Champions, cinq ans après sa défaite contre le Bayern,
- La remontada de l'Inter face au Barça en 1/2 finale retour pour aller défier le PSG en finale,
- L'élimination des Lakers de LeBron James et Luka Dončić par les Timberwolves d'Anthony Edwards...

et avec encore beaucoup de spectacle attendu, notamment pendant la suite du mois de mai.

Pour celles et ceux qui souhaitent (re)découvrir les vainqueurs des grandes compétitions passées, ce projet permet d'obtenir rapidement :

- Les champions NBA ou d'une ligue de football donnée pour une année spécifique.
- Les statistiques détaillées des joueurs de l'équipe victorieuse pour cette année.

## ⚙️ Fonctionnalités

Les informations sont renvoyées par un agent IA, capable donc de répondre par exemple à des questions du type :

> "Qui a gagné la Bundesliga en 2017 ?"

Il s'appuie sur deux outils pour fournir une réponse complète et contextualisée :

### 🏀 NBA
- `get_nba_champions_mvp_stats_table(year: int)`  
  Renvoie :
  - Les champions NBA
  - Le MVP de la saison
  - Un tableau des statistiques individuelles des joueurs

### ⚽ Football
- `get_football_champions_stats_table(league: str, year: int)`  
  Renvoie :
  - Les champions de la ligue (Ligue 1, Premier League, etc.)
  - Un tableau des statistiques individuelles des joueurs

On fournit également, dans le but de s'assurer que l'agent fasse le bon choix d'outils selon la requête demandée, un outil de recherche web ainsi que des outils d'addition et de soustraction d'entiers.

Les informations sont récupérées depuis les sites [🏀 Basketball Reference](https://www.basketball-reference.com/) et [⚽ Football Reference](https://fbref.com/fr/)

## 💻 Environnement

- [VSCodium 1.99.32846](https://github.com/VSCodium/vscodium/releases)
- Anaconda3 2024.10-1
- [Python 3.12.7](https://www.python.org/downloads/)

## 🚀 Utilisation

Pour installer les dépendances, on utilise [uv](https://docs.astral.sh/uv/) :
> pip install uv

Pour lancer le script :
> uv run main.py

❗ **Il faudra au préalable veiller à fournir une clé API [Groq](https://groq.com/) dans un fichier** `.env` :
> GROQ_API_KEY = "your-API-key"

Pour installer les dépendances manuellement :
> uv add agno groq python-dotenv duckduckgo-search
>
> uv add pandas bs4 fuzzywuzzy python-Levenshtein
>
> uv add requests==2.27.1

## 📸 Exemples d'utilisation

*NBA : années 2018 & 2021*

![b-n2_n1](https://github.com/user-attachments/assets/1ccce717-4d00-4de2-9e75-9452a6a348c8)

*Football : Serie A, 2014*

![f-n2_n1](https://github.com/user-attachments/assets/3a83449b-9064-4f6f-9978-9bcde86eb5de)
