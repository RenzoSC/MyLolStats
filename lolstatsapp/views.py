from django.shortcuts import render
from . import req

# Create your views here.
def home(request):
    
    return render(request, "home.html")

def search(request):
    sum=req.fetchSumByName(request.GET["summoner_name"])
    summoner_info = req.get_summoner_info(sum["id"])
    matchs_info = req.getMatchList(sum["puuid"])
    matchs_info = req.lastmatches_info(matchs_info, request.GET["summoner_name"])
    topchamps = [matchs_info[1]["champs_used"][champ] for champ in sorted(matchs_info[1]["champs_used"], key=lambda x: matchs_info[1]["champs_used"][x]['kda'], reverse=True)[:3]]
    return render(request,"sum.html",{
        "summonerName": sum["name"],
        "summonerLevel": sum["summonerLevel"],
        "summonerInfo": summoner_info,
        "summonerIcon" : sum["profileIconId"],
        "matches": matchs_info[0],
        "matches_info": matchs_info[1],
        "totalMatchs" : matchs_info[1]["totalWins"] + matchs_info[1]["totalDef"],
        "topchamps" : topchamps,
    })