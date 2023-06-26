from django.shortcuts import render
import requests

riotkey = "RGAPI-7c2d8ac2-7025-40f2-b544-f2ce87ceaf2a"

# Create your views here.
def home(request):
    fetchSumByName("Vinde")
    return render(request,"home.html")

def fetchSumByName(name, opt_get):
    """
    returns the data (opt_get) from a summoner searched by name

    (String) opt_get could be:
        - id --> summonerId /encryptedSummonerId
        - accountId --> accountId / encryptedAccountId
        - puuid --> PUUID / enctryptedPUUID
        - name --> summoner name
        - profileIconId --> summoner icon
        - revisionDate --> Date summoner was last modified specified as epoch milliseconds
        - summonerLevel --> level of summoner
    """
     
    url = f"https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0",
        "Accept-Language": "es,es-419;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        'X-Riot-Token': riotkey,
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data[opt_get]
    else:
        print("Error:", response.status_code)
        return None
    
def getMatchList(puuid, count=20):
    """
    returns a list of match where index 0 is the most recent and index /count/ is the oldest

    (String) puuid --> summoner's puuid
    (Int) count --> number in range 0-100, number of matchs that the function will get
    """

    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0",
        "Accept-Language": "es,es-419;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": riotkey
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        return None
    
def last20matches_info(matches, name):
    """
    returns an array[0..19] with info from the last 20 matches
    """
    matches_data = []

    for match in matches:
        data = {}
        data["gameMode"] = match["info"]["gameMode"]
        data["duration"] = match["info"]["gameDuration"]
        data["teamKills"] = 0
        data["enemyKills"] = 0
        
        for participant in match["info"]["participants"]:
            if participant["summonerName"] == name:
                data["win"] = participant["win"]
                data["champId"] = participant["championId"] 
                data["champName"] = participant["championName"]
                data["champLevel"] = participant["championLevel"]
                data["kills"] = participant["kills"]
                data["deaths"] = participant["deaths"]
                data["assists"] = participant["assists"]
                data["kda"] = participant["challenges"]["kda"]
                data["kill-participation"] = participant["challenges"]["killParticipation"]
                data["pink-wards"] = participant["visionWardsBoughtInGame"]
                data["cs"] = participant["totalMinionsKilled"] + participant["neutralMinionsKilled"]
                data["item0"] = participant["item0"]
                data["item1"] = participant["item1"]
                data["item2"] = participant["item2"]
                data["item3"] = participant["item3"]
                data["item4"] = participant["item4"]
                data["item5"] = participant["item5"]
                data["item6"] = participant["item6"]
                data["primary-rune"] = participant["perks"]["styles"][0]["style"]
                data["secondary-rune"] = participant["perks"]["styles"][1]["style"]
        
        for participant in match["info"]["participants"]:
            if participant["win"] == data["win"]:
                data["teamKills"] += participant["kills"]
            else:
                data["enemyKills"] += participant["kills"]

        matches_data.append(data)

    return data