import sys
import json

credentials = json.loads(sys.argv[1])

token = sys.argv[2]
#token_expiry = sys.argv[3]

with open('token.json', 'w') as token_file:
    json.dump({"token": token,
               "token_uri": "https://oauth2.googleapis.com/token",
               "client_id": credentials["installed"]["client_id"],
               "client_secret": credentials["installed"]["client_secret"],
               "scopes": [
                   "https://www.googleapis.com/auth/calendar"
               ],
               "refresh_token": ""
               # "expiry": token_expiry,
               }, token_file)
