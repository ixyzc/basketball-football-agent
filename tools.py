import re
import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup, Comment

from fuzzywuzzy import process


def add_numbers(a: int, b: int):
    return a + b


def substract_numbers(a: int, b: int):
    return a - b


def get_nba_champions_mvp_stats_table(year: int):
    """
    Récupère les champions NBA et le MVP d'une année donnée,
    ainsi que les stats de chaque joueur de l'équipe gagnante.

    :param year: année de la saison NBA
    :return: les champions de la saison, le MVP de la saison,
    ainsi qu'un tableau contenant les stats de chaque joueur de l'équipe gagnante.
    """

    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
    response = requests.get(url)
    data = response.text

    # Parsing pour récupérer 1. l'équipe gagnante, ainsi que 2. le MVP
    # 1. example (2010) : <strong>League Champion</strong>: <a href=\'/teams/LAL/2010.html\'>Los Angeles Lakers</a>
    # 2. example (2010) : <strong>Most Valuable Player</strong>: <a href=\'/players/j/jamesle01.html\'>LeBron James</a>
    champions_pattern = r"<strong>League Champion</strong>: <a [^>]*>(.*?)</a>"
    mvp_pattern = r"<strong>Most Valuable Player</strong>: <a [^>]*>(.*?)</a>"
    abb_pattern = (
        r"<strong>League Champion</strong>: <a href='/teams/([^/]+)/\d{4}.html'>"
    )

    # Search
    champions_match = re.search(champions_pattern, data)
    mvp_match = re.search(mvp_pattern, data)
    abb_match = re.search(abb_pattern, data)

    # Match
    champions = champions_match.group(1)
    mvp = mvp_match.group(1)
    team_abb = abb_match.group(1)

    # Maintenant que l'on a toutes ces informations...
    url = f"https://www.basketball-reference.com/teams/{team_abb}/{year}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Trouver la table avec l'id 'totals_stats'
    table = soup.find("table", {"id": "totals_stats"})

    if table is None:  # si non trouvée : c'est qu'elle est dans un commentaire
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if "totals_stats" in comment:
                table_soup = BeautifulSoup(comment, "html.parser")
                table = table_soup.find("table", {"id": "totals_stats"})
                break

    # Lecture de la table HTML comme une DataFrame
    df = pd.read_html(StringIO(str(table)))[0]

    # cols = ["Player", "Age", "PTS", "AST", "FT", "FTA", "STL", "BLK", "ORB", "DRB", "TRB"]
    cols = ["Player", "Age", "PTS", "AST", "FT", "STL", "BLK", "TRB"]
    df = (
        df.iloc[:-1, :][cols]
        .sort_values(["PTS", "AST"], ascending=False)
        .reset_index(drop=True)
        .astype({"Age": "int32"})
    )

    df.rename(
        columns={
            "PTS": "Points",
            "AST": "Assists",
            "FT": "Free Throws",
            # "FTA": "Free Throws Attempts",
            "STL": "Steals",
            "BLK": "Blocks",
            # "ORB": "Offensive Rebounds",
            # "DRB": "Defensive Rebounds",
            "TRB": "Rebounds",
        },
        inplace=True,
    )

    # display(df)
    return champions, mvp, df


def get_football_champions_stats_table(league: str, year: int):
    """
    Récupère les champions d'une ligue de football d'une année donnée,
    ainsi que les stats de chaque joueur de l'équipe gagnante.

    :param league: ligue de football considérée
    :param year: année de la saison considérée
    :return: les champions de la ligue pour la saison donnée,
    le(s) meilleur(s) buteur(s) et leur nombre de buts,
    le(s) meilleur(s) passeur(s) et leur nombre de passes décisives,
    ainsi qu'un tableau contenant les stats de chaque joueur de l'équipe gagnante.
    """

    league_ids = {
        "Champions League": 8,
        "Europa League": 19,
        # "Coupe du Monde": 1, #"Euro": 676, #"Copa América": 685,
        "Premier League": 9,
        "Serie A": 11,
        "La Liga": 12,
        "Ligue 1": 13,
        "Bundesliga": 20,
        "Primera División": 21,
        "MLS": 22,
        "Eredivisie": 23,
        "Primeira Liga": 32,
        "Saudi Professional League": 70,
    }

    league_urls = {
        ln: f"https://fbref.com/en/comps/{league_ids[ln]}/{year}-{year + 1}"
        for ln in league_ids.keys()
    }

    country_to_league_dict = {}
    country_to_league_dict.update(
        dict.fromkeys(["Angleterre", "Anglaise"], "Premier League")
    )
    country_to_league_dict.update(dict.fromkeys(["Italie", "Italienne"], "Serie A"))
    country_to_league_dict.update(dict.fromkeys(["Espagne", "Espagnole"], "La Liga"))
    country_to_league_dict.update(dict.fromkeys(["France", "Française"], "Ligue 1"))
    country_to_league_dict.update(
        dict.fromkeys(["Allemagne", "Allemande"], "Bundesliga")
    )
    country_to_league_dict.update(dict.fromkeys(["Argentine"], "Primera División"))
    country_to_league_dict.update(
        dict.fromkeys(["USA", "Amérique", "Américaine"], "MLS")
    )
    country_to_league_dict.update(
        dict.fromkeys(["Pays-Bas", "Néerlandaise"], "Eredivisie")
    )
    country_to_league_dict.update(
        dict.fromkeys(["Portugal", "Portuguaise"], "Primeira Liga")
    )
    country_to_league_dict.update(
        dict.fromkeys(["Arabie", "Saoudite", "Saoudienne"], "Saudi Professional League")
    )

    # Possibilité d'une faute de frappe lors de l'entrée de la ligue
    league_name, score1 = process.extractOne(league, league_urls.keys())
    country, score2 = process.extractOne(league, country_to_league_dict.keys())

    if score1 > score2:
        league = league_name
        url = league_urls[league_name]
    else:
        league = country_to_league_dict[country]
        url = league_urls[league]

    response = requests.get(url)
    data = response.text
    # # response.status_code = 403 with requests==2.32.3 ☒
    # # response.status_code = 200 with requests==2.27.1 ☑

    # Parsing pour récupérer 1. l'équipe gagnante, ainsi que 2. le(s) meilleur(s) buteur(s), et 3. le(s) meilleur(s) passeur(s)
    # 1. example (Serie A 2010) : <strong>Champion</strong>: <img ...> <a ...>Milan</a>
    # 2. example (Serie A 2010) : <strong>Most Goals</strong>: <a ...>Antonio Di Natale</a> (Udinese) - <span>28</span>
    # 3. example (Serie A 2010) : <strong>Most Assists</strong>: <a ...>Ezequiel Lavezzi</a> (Napoli) - <span>13</span>
    champions_pattern = r"<strong>Champion</strong>: <img [^>]*> <a [^>]*>(.*?)</a>"
    topGLS_pattern = (
        r"<strong>Most Goals</strong>: <a [^>]*>(.*?)</a> (.*?) - <span>(\d+)</span>"
    )
    topAST_pattern = (
        r"<strong>Most Assists</strong>: <a [^>]*>(.*?)</a> (.*?) - <span>(\d+)</span>"
    )

    champions_match = re.search(champions_pattern, data)
    topGLS_match = re.search(topGLS_pattern, data)
    topAST_match = re.search(topAST_pattern, data)

    champions = champions_match.group(1)
    topGLS, nGLS = (
        " ".join([topGLS_match.group(1), topGLS_match.group(2)]),
        topGLS_match.group(3),
    )
    topAST, nAST = (
        " ".join([topAST_match.group(1), topAST_match.group(2)]),
        topAST_match.group(3),
    )

    topGLS, topAST = [topGLS], [topAST]

    if "," in topGLS[0]:
        # exemple : https://fbref.com/en/comps/11/2014-2015 (Serie A 2014)
        j1_pattern = r"^[^,]+"
        j1 = re.search(j1_pattern, topGLS[0]).group(0)

        j2_pattern = r"<a [^>]*>(.*?)</a> (\(.*?\))[...]{0,1}"  # il PEUT y avoir des ... à la fin !!!
        j2 = re.search(j2_pattern, topGLS[0])
        nomj2, clubj2 = j2.group(1), j2.group(2)
        j2 = " ".join([nomj2, clubj2])

        topGLS = [j1, j2]

    if "," in topAST[0]:
        # exemple : https://fbref.com/en/comps/11/2014-2015 (Serie A 2014)
        j1_pattern = r"^[^,]+"
        j1 = re.search(j1_pattern, topAST[0]).group(0)

        j2_pattern = r"<a [^>]*>(.*?)</a> (\(.*?\))[...]{0,1}"  # il PEUT y avoir des ... à la fin !!!
        j2 = re.search(j2_pattern, topAST[0])
        nomj2, clubj2 = j2.group(1), j2.group(2)
        j2 = " ".join([nomj2, clubj2])

        topAST = [j1, j2]

    # print(f"The Team who won the {league} in {year} was: {champions}")
    # print("The Top Scorer(s) that year:", " & ".join(topGLS), f"with {nGLS} goals")
    # print(
    #     "The Player(s) with the most Assists:",
    #     " & ".join(topAST),
    #     f"with {nAST} assists",
    # )

    # We're sorry, but we don't yet cover this competition
    # (https://fbref.com/en/comps/21/2008-2009) for example

    # Maintenant que l'on a toutes ces informations...
    soup = BeautifulSoup(response.text, "html.parser")
    champion_strong = soup.find("strong", string="Champion")
    a_tag = champion_strong.find_next("a")
    url = f"https://fbref.com{a_tag['href']}#all_stats_standard"

    # GET request pour fetch le page content
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Trouver la table avec l'id 'stats_standard_{league_id}'
    league_id = league_ids[league]
    table = soup.find("table", {"id": f"stats_standard_{league_id}"})

    if table is None:  # si non trouvée : c'est qu'elle est dans un commentaire
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if f"stats_standard_{league_id}" in comment:
                table_soup = BeautifulSoup(comment, "html.parser")
                table = table_soup.find("table", {"id": f"stats_standard_{league_id}"})
                break

    # Lecture de la table HTML comme une DataFrame
    df = pd.read_html(StringIO(str(table)))[0]
    df.columns = df.columns.droplevel()  # car la DataFrame a un multi-index

    # "Player", "Pos", "Age", "MP", "Starts", "Min", "Gls", "Ast", "Penalty Goals","Penalty Attemps", "Yellow Cards", "Red Cards"
    df = (
        df.iloc[:-2, [0, 2, 3, 4, 5, 6, 8, 9, 12, 13, 14, 15]]
        .sort_values(["Gls", "Ast"], ascending=False)
        .reset_index(drop=True)
        .fillna(0)
        .astype({"Age": "int32"})
    )
    df.rename(
        columns={
            "Pos": "Position(s)",
            "MP": "Matches Played",
            "Starts": "Games Started",
            "Min": "Minutes Played",
            "Gls": "Goals",
            "Ast": "Assists",
            "PK": "Penalties Scored",
            "PKatt": "Penalty Attempts",
            "CrdY": "Yellow Cards",
            "CrdR": "Red Cards",
        },
        inplace=True,
    )

    smaller_df = df[
        [
            "Player",
            "Position(s)",
            "Age",
            "Matches Played",
            "Goals",
            "Assists",
        ]
    ]

    # display(df)
    # display(smaller_df)

    return champions, " & ".join(topGLS), nGLS, " & ".join(topAST), nAST, smaller_df
