import requests
from bin.constants import API_KEY

def get_movie(title:str) -> dict:
    try:
        return requests.get(f'http://www.omdbapi.com/?&apikey={API_KEY}&t={title}').json()
    except Exception as e:
        return {'Response': 'False', 'Error': f'{e}'}