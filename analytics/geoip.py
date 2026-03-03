import requests

def get_country(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        return data.get("country", "Unknown")
    except:
        return "Unknown"
