# import sys
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from tools import get_nba_champions_mvp_stats_table
from tools import get_football_champions_stats_table
from tools import add_numbers, substract_numbers

# print("Python executable:", sys.executable)
load_dotenv()

tools = [
    DuckDuckGoTools(fixed_max_results=3),
    add_numbers,
    substract_numbers,
    get_nba_champions_mvp_stats_table,
    get_football_champions_stats_table,
]
agent = Agent(
    model=Groq(
        # id="llama-3.3-70b-versatile",
        id="llama-3.1-8b-instant",
        response_format={"type": "json_object"},
    ),
    tools=tools,
    show_tool_calls=True,
    instructions=[
        "Veiller à bien espacer les différents résultats les uns des autres.",
        "Si des statistiques doivent être affichées, le faire à l'aide d'un tableau.",
        "S'il y a des termes en anglais, il faudra veiller à les traduire en français.",
        "Si l'utilisateur a posé plusieurs questions, il faudra écrire une conclusion à la fin",
    ],
    markdown=True,
)

print("\n> uv run main.py\n")

# prompt = "Qui a gagné la NBA en 2011 ? Quelles sont les statistiques de chaque joueur ? Combien font 5 plus 4 ?"

# agent.print_response(prompt)

# prompt = "Qui a gagné la NBA en 2018 ? Quelles sont les statistiques de chaque joueur ? Peux-tu répondre aussi pour l'année 2021 ? Et combien font vingt plus quatre cent deux ? Enfin, quelle est la température à Paris aujourd'hui ?"

# agent.print_response(prompt)

prompt = "Qui a gagné la ligue de football italienne en 2014 ? J'aimerais aussi savoir qui a été le meilleur buteur et le meilleur passeur de cette saison. Peux-tu me donner les statistiques de chaque joueur ?"

agent.print_response(prompt)

# prompt = input("Enter your prompt: ")
# while prompt != "":
#     agent.print_response(prompt)
#     prompt = input("Enter your prompt: ")

"""
We recommend using llama-3.3-70b-versatile for general use
We recommend llama-3.1-8b-instant for a faster result.
We recommend using llama-3.2-90b-vision-preview for image understanding.
"""
