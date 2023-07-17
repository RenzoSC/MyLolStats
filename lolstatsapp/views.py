from django.shortcuts import render
import requests

riotkey = "RGAPI-6c97554a-bc9c-4bb1-8518-cecfd0a5df24"

# Create your views here.
def home(request):
    sum=fetchSumByName("Vinde")
    summoner_info = get_summoner_info(sum["id"])
    matchs_info = getMatchList(sum["puuid"])
    matchs_info = lastmatches_info(matchs_info, "Vinde")
    return render(request,"home.html",{
        "summonerName": sum["name"],
        "summonerLevel": sum["summonerLevel"],
        "summonerInfo": summoner_info,
        "summonerIcon" : sum["profileIconId"],
        "matches": matchs_info[0],
        "matches_info" : matchs_info[1]
    })

def fetchSumByName(name):
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
        return data
    else:
        print("Error: fe ", response.status_code)
        return None
    
def getMatchList(puuid, count=10):
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
        print("Error: ge ", response.status_code)
        return None
    
def lastmatches_info(matches, name):
    """
    returns an array[0..matches.len] with info from the last matches.len matches
    """
    matches_data = [[],{}]
    queue_type = {400:"Normal reclutamiento", 420:"SoloQ", 430:"Normal", 440:"Flexible", 450:"Aram"}
    matches_data[1]["totalWins"] = 0
    matches_data[1]["totalDef"] = 0
    for match in matches:
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0",
            "Accept-Language": "es,es-419;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": riotkey
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            match = response.json()
            data = {}
            y =match["info"]["queueId"]
            data["gameMode"] = queue_type[y]
            data["duration"] = match["info"]["gameDuration"]
            data["teamKills"] = 0
            data["enemyKills"] = 0
            
            for participant in match["info"]["participants"]:
                if participant["summonerName"] == name:
                    if participant["win"]:
                        data["win"] = "Victoria"
                        matches_data[1]["totalWins"] +=1
                    else:
                        data["win"] = "Derrota"
                        matches_data[1]["totalDef"] +=1
                    data["win_b"] = participant["win"]
                    data["champId"] = participant["championId"] 
                    data["champName"] = participant["championName"]
                    data["champLevel"] = participant["champLevel"]
                    data["kills"] = participant["kills"]
                    data["deaths"] = participant["deaths"]
                    data["assists"] = participant["assists"]
                    data["kda"] = format(participant["challenges"]["kda"], ".2f")
                    data["killParticipation"] = int(float(format(participant["challenges"]["killParticipation"],".2f"))*100)
                    data["pinkWards"] = participant["visionWardsBoughtInGame"]
                    data["cs"] = participant["totalMinionsKilled"] + participant["neutralMinionsKilled"]
                    data["items"] = [participant["item0"],participant["item1"],participant["item2"],participant["item3"],participant["item4"],participant["item5"],participant["item6"]]
                    data["spell1"] = participant["summoner1Id"]
                    data["spell2"] = participant["summoner2Id"]
                    data["primary-rune"] = participant["perks"]["styles"][0]["style"]
                    data["secondary-rune"] = participant["perks"]["styles"][1]["style"]
            data["teamsSummoners"] = [[],[]] 

            for participant in match["info"]["participants"]:
                summoner = {}
                if participant["win"] == data["win_b"]:
                    data["teamKills"] += participant["kills"]
                else:
                    data["enemyKills"] += participant["kills"]

                x = 0 if participant["teamId"] == 100 else 1        
                
                summoner["name"] = participant["summonerName"]
                summoner["champ"] = participant["championName"]
                data["teamsSummoners"][x].append(summoner)
            matches_data[0].append(data)
        else:
            print("Error: la", response.status_code)
            return None
        
    return matches_data

def get_summoner_info(sumid):
    """
    returns an array with info from index 0 : SoloQ // index 1: Flex
    
    The elements from the array has this keys:
        - leagueId --> the summoner's league id
        - queueType --> (RANKED_SOLO_5x5/RANKED_FLEX_SR)
        - tier --> the summoner's league (IRON/BRONZE/ETC)
        - rank --> tier divison (I, II, III, IV)
        - summonerId --> summoner ID
        - summonerName --> summoner name
        - leaguePoints --> LP
        - wins --> # of games that summoner won on that queueType
        - losses --> # of games that summoner lost on that queueType
        - veteran
        - inactive
        - freshBlood
        - hotStreak
    """
    url = f"https://la2.api.riotgames.com/lol/league/v4/entries/by-summoner/{sumid}"

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
        for info in data:
            info["winrate"] = int((info["wins"]/(info["wins"] + info["losses"]))*100)
            info["tier"] = info["tier"].lower()
            if info["queueType"] == 'RANKED_SOLO_5x5':
                info["queueType"] = "SoloQ"
            elif info["queueType"]  == 'RANKED_FLEX_SR':
                info["queueType"] = "Flexible"
        return data
    else:
        print("Error: sum", response.status_code)
        return None
    