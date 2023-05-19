import requests

def get_motorcycles(make, model):
    api_key = 'YOUR_API_KEY'  # Замените на ваш API-ключ
    url = f'https://api.motorcycle-data.com/v1/motorcycles?make={make}&model={model}&apikey={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
