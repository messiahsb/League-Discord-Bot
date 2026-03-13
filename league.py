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
    match_list = list(map(Match, data))
    print(data)
    return match_list

def get_match_data(match_id:str = None):
    match_endpoint = f"/lol/match/v5/matches/{match_id}"
    match_request = requests.get(ROOT + match_endpoint + "?api_key=" + L_KEY) 
    data = match_request.json()
    return data

def get_match_history_data(match_data: list[Match]): 
    for i in match_data:
        print((i.get_match_data())['info']["participants"][0]["win"])

class Match:

    def __init__(self, matchID):
        self.__matchID = matchID
        # self.__win 

    def __str__(self):
        return f"({self.__matchID})"

    def get_matchID(self):       
        return f"{self.__matchID}"
    
    def get_match_data(self):
        match_endpoint = f"/lol/match/v5/matches/{self.__matchID}"
        match_request = requests.get(ROOT + match_endpoint + "?api_key=" + L_KEY) 
        data = match_request.json()
        return data 

    
history = get_match_history(get_puuid("Wold5182", "NA1"))
# print(get_match_data(history[0].get_matchID()))

# for i in history:
#     print(i)
print(get_match_history_data(history))
    # get match history--> loop through history using async to get each individual match data, 
    # store that data in list to be accessed later
    # this will be the real get match history class, so I do not have to display a bunch of IDs

