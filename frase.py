import requests

class CNQuotes:

    def __init__(self):
        self.url = 'https://api.chucknorris.io/jokes/random'
        self.quote = ''
        self.get_quote()

    def get_quote(self):
        with requests.get(url=self.url) as data:
            quote = data.json()['value']

        self.quote = quote
