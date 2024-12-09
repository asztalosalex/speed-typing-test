import requests

class RandomWordAPI:

    RANDOM_WORD_API_URL = "https://random-word-api.herokuapp.com/word"


    def __init__(self):
        self.url = self.RANDOM_WORD_API_URL
    

    def get_random_words(self, count: int)->list[str]:
        response = requests.get(self.url, params={"number": str(count)})
        if response.status_code != 200:
            raise Exception(f"Failed to get random words: {response.status_code}")
        return response.json()
    
