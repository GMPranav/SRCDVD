import requests

client_id = input("Enter Client-ID: ")
client_secret = input("Enter Client Secret: ")

body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)

#data output
keys = r.json();

print("\nyour access token is: "+keys['access_token'])
dummy = input("\n\nCopy down your token and press any key to exit")