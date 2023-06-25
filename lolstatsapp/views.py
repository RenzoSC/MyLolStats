from django.shortcuts import render
import requests

# Create your views here.
def home(request):
    fetchSumByName("Vinde")
    return render(request,"home.html")

def fetchSumByName(name):
    riotkey = "RGAPI-3ea9db1f-72d5-4b74-9728-586d9a435581"  # Reemplaza "TU_API_KEY" con tu propia clave de API
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
        print(data["summonerLevel"])
        return data["summonerLevel"]
    else:
        print("Error:", response.status_code)
        return None