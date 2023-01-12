import json

def save_token_to_file(token, filename="token.json"):
    """Saves a token dictionary to a json file"""
    with open(filename, "w") as fp:
        json.dump(token, fp, sort_keys=True, indent=4)