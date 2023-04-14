import sys
import os
import aiohttp
import asyncio
import json
from fpl import FPL
from dotenv import load_dotenv

load_dotenv()


async def my_league(league_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)

        userEmail = os.getenv("EMAIL")
        userPassword = os.getenv("PASSWORD")
        await fpl.login(email=userEmail, password=userPassword)

        league_json = await fpl.get_classic_league(league_id, return_json=True)

        entries_list = []

        # *Create a list for the entries
        for entry in league_json['standings']['results']:

            entry_dict = {
                'id': entry['id'],
                'Name': entry['entry_name'],
                'Total': entry['total'],
                'Event_total': entry['event_total']
            }

            entries_list.append(entry_dict)

        # *Sort the entries

        entries_list.sort(key=lambda x:x['Event_total'], reverse=True)

        # **Sorted list
        for entry in entries_list:

            print(entry['id'], entry['Name'], entry['Total'], entry['Event_total'])

# Function to save a list to json file
def saveJson(json_file):
    with open('league_details', 'w') as outputfile:
        json.dump(json_file, outputfile)


if sys.version_info >= (3, 7):
    # Python 3.7+
    asyncio.run(my_league(os.getenv("LEAGUE_ID")))

else:
    # Python 3.6
    loop = asyncio.get_event_loop()
    loop.run_until_complete(my_league(os.getenv("LEAGUE_ID")))
