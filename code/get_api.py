import requests

#Url: https://api.open-meteo.com/v1/forecast?latitude=21.0245&longitude=105.8412&hourly=temperature_2m&timezone=Asia%2FSingapore
base_url = r"https://api.open-meteo.com"
end_point = r"v1/forecast"

def get_api(lat, lon, timezone):

    url = f"{base_url}/{end_point}?latitude={lat}&longitude={lon}&hourly=temperature_2m&timezone={timezone}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        print(f"Your current url: {url}")
        return f"Wrong url"
    else:
        return response.status_code

