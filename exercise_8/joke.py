import requests

r = requests.get ("https://icanhazdadjoke.com/" , headers={ "Accept": "text/plain"})
print(r.text)
