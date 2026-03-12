import requests
import os
from dotenv import load_dotenv
import pandas as pd

# load hidden API Key
load_dotenv()
L_KEY = os.getenv("L_API")

# url to call api from with different endpoints
ROOT = "https://americas.api.riotgames.com/"

# Function for getting the player PUUID from gameName and tagLine
def get_puuid(gameName:str = None, tagLine : str = None) -> str: 

    id_endpoint = f"riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    id_request = requests.get(ROOT + id_endpoint + "?api_key=" + L_KEY) 
    data = id_request.json()
    puuid = data["puuid"]

    return puuid

# Function for getting the player gameName and tagLine through PUUID
def get_player(puuid:str = None) -> dict[str, str]: 
    
    player_endpoint = f"/riot/account/v1/accounts/by-puuid/{puuid}/"
    player_request = requests.get(ROOT + player_endpoint + "?api_key=" + L_KEY) 
    data = player_request.json()
    player: dict = {data["gameName"], data["tagLine"]}

    return player

def get_match_history(puuid:str = None, start: str = 0, count: str = 20) -> list:

    match_endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    match_request = requests.get(ROOT + match_endpoint + "&api_key=" + L_KEY) 
    data = match_request.json()
    return data

def get_match_data(match_id:str = None):
    match_endpoint = f"/lol/match/v5/matches/{match_id}"
    match_request = requests.get(ROOT + match_endpoint + "?api_key=" + L_KEY) 
    data = match_request.json()
    return data

def get_match_winner(match_data):
    print(match_data['info']["participants"][0]["win"])

matchid = (get_match_history("vDWCMdm4Cmdgwetkt-euNs4otmWPe24Vzts1-l9_6orNo5_dLFhU61CNwH-P7IAuXadRBHiS-6Gu_Q", "0", "1"))
# print(matchid.type())
# print(get_match_data(matchid[0]))
get_match_winner(get_match_data(matchid[0]))
