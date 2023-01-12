from monzopy.classes.auth import MonzoAuthClient
from monzopy.classes.monzo import Monzo
import json

with open("client.json", "r") as f:
    client_info = json.load(f)

client_id = client_info['client_id']
client_secret = client_info['client_secret']

url = "http://127.0.0.1:8000"
authClient = MonzoAuthClient(client_id=client_id, client_secret=client_secret)

auth_url = authClient.create_authorization_url(redirect_uri=url)
print(auth_url)

authClient.first_auth(redirect_uri=url)

authClient.auth_from_file()

MonzoApi = Monzo(auth_client=authClient)

data = MonzoApi.get_pots()
for item in data:
    print(f"Pot: {item['name']}")
    print(f"Pot Balance: {item['balance']}")