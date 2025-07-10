MSG_MOVIE_DOESNT_EXIST = "This movie doesn't exist!"
MSG_RATING_IS_NOT_NUMERIC = "Rating is not a number!"
MSG_INVALID_INPUT = "Invalid Input!"
MSG_NO_RESULTS = 'No Results!'
MSG_WRONG_RATING = "Enter a rating in range: 0 - 10"
MSG_KINETOSSCOPE_NOT_INVENTED_YET = 'Please enter a value above 1891! https://en.wikipedia.org/wiki/Kinetoscope'
MSG_NO_TITLE = 'No title given!'


MOVIE_PATH = 'movies\\'

MAX_RATING = 10
YEAR = 'year'
RATING = 'rating'

class APIKeyNotProvidedError(Exception):
    """
Provide an apikey. 
To do this:
1. Create a ".env" file in root
2. enter > apikey={yourkey} & save
    """

from dotenv import load_dotenv
from os import getenv
from bin.modules import error
loaded = load_dotenv('.env')
API_KEY = getenv('apikey')
if not API_KEY or not loaded:
    raise APIKeyNotProvidedError()