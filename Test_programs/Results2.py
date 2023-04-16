import requests
import os
import json
from dotenv import load_dotenv
import time

load_dotenv()


def my_league(league_id):
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/"
    session = requests.session()
    userEmail = os.getenv("EMAIL")
    userPassword = os.getenv("PASSWORD")
    login_url = "https://users.premierleague.com/accounts/login/"
    payload = {
        "login": userEmail,
        "password": userPassword,
        "redirect_uri": "https://fantasy.premierleague.com/a/login",
        "app": "plfpl-web"
    }
    session.post(login_url, data=payload)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to get league data")

    league_json = response.json()

    entries_list = []

    for entry in league_json['standings']['results']:
        entry_dict = {
            'id': entry['entry'],
            'Name': entry['entry_name'],
            'Total': entry['total'],
            'Event_total': entry['event_total']
        }

        entries_list.append(entry_dict)

    entries_list.sort(key=lambda x: x['Event_total'], reverse=True)

    for entry in entries_list:
        print(entry['id'], entry['Name'], entry['Total'], entry['Event_total'])


start_time = time.time()
my_league(os.getenv("LEAGUE_ID"))

end_time = time.time()

print("---------------------------------- \n")

print(f"Execution time: {end_time - start_time} seconds")
