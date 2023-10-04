import requests

FRED_API_KEY = "FRED_API_KEY"

def USTreasury10YrRate():
    series = "DGS10"
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series}&api_key={FRED_API_KEY}&file_type=json"
    response = requests.get(url)
    data = response.json()
    return float(data['observations'][0]['value'])

if __name__ == "__main__":
    print(USTreasury10YrRate())