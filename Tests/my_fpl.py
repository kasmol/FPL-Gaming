from fpl import FPL
import aiohttp
import sys
import asyncio
import json

async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        player= await fpl.get_player(335, return_json=False)
        #print(player)
        #print(player["total_points"])
        #print(player.points_per_game)

#auuthentiating to my team
async def my_team(user_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email="Otienomoses998@gmail.com",password="Moseti92278783#")
        user= await fpl.get_user(user_id)
        team= await user.get_team()
        chips = await user.get_chips()
        #print(chips)

        #get user league
        league_json=await fpl.get_classic_league(2390172, return_json=True)
        #converting json data to a list
        entries_list=[]
        for entry in league_json["standings"]["results"]:
            #print for me the list
            #print(entry["rank"],entry["id"], entry["entry_name"], entry["total"], entry["event_total"])
            #let's find the event winner
            entry_dict={
                "rank":entry["rank"],
                "id": entry["id"],
                "entry_name":entry["entry_name"],
                "event_total": entry["event_total"],
                "total": entry["total"]
            }
            entries_list.append(entry_dict)
        #sorting the entries
        entries_list.sort(key=lambda x:x["event_total"],reverse=True)

        #final sorted data
        for entry in entries_list:
            print(entry["rank"],entry["id"], entry["entry_name"], entry["total"], entry["event_total"])
        
        
        

if sys.version_info >= (3,7):
    #for python 3.7+
    asyncio.run(main())
    #in my team
    #asyncio.run(my_team())
    asyncio.run(my_team(10726628))
else:
    #for python 3.6
    loop= asyncio.get_event_loop()
    loop.run_until_complete(main())


