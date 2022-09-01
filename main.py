allP = 0
import twitchio
from twitchio.ext import pubsub
import json
import ftplib

print("ACCESS TOKEN брать тут - https://twitchtokengenerator.com/")
print("oAuth брать тут - https://twitchapps.com/tmi/")
print("ID аккаунта брать тут - https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/")

oauth = input("Введи oAuth код (без oauth: в начале): ")
token = input("Введи токен: ")
accid = input("Введи ID акаунта: ")
logg = input('Включить логи в консоли? (1 - да): ') or "0"
# Fill Required Information
HOSTNAME = "s221138.hostiman.com"
USERNAME = "mjkey_dex"
PASSWORD = "123123"

# Connect FTP Server
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
 
# force UTF-8 encoding
ftp_server.encoding = "utf-8"

try:
    f = open("data.json")
except:
    data = {
        "allPoints": allP,
        "users": {}
    }
    with open("data.json","w") as w: 
        json.dump(data,w)
    w.close()

# my_token = "8zopstc1u5ydh7q2b69ylmtip906d9" #oauth
# users_oauth_token = "sxjx3672u4ybybgy4brsfgqiowbmui" #accestokken
my_token = oauth #oauth
users_oauth_token = token #accestokken
users_channel_id = int(accid) #180238325
client = twitchio.Client(token=my_token)
client.pubsub = pubsub.PubSubPool(client)

@client.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    if logg == "1":
        print(event.user.id)
        print(event.user.name)
        print(event.reward.cost)
    f = open("data.json", "r")
    b = json.load(f)
    f.close()
    b["allPoints"]+=event.reward.cost
    if str(f'{event.user.id}') in b['users']:
        b['users'][str(f'{event.user.id}')]['points'] = b['users'][str(f'{event.user.id}')]['points'] + event.reward.cost
    else:
        b['users'][str(f'{event.user.id}')] = {
            'points': event.reward.cost,
            'nick' : event.user.name
        }
    f = open("data.json", "w")
    json.dump(b,f,indent=4)
    if logg == "1":
        print(b)
    f.close()
    

    filename = 'data.json'
    with open(filename, "rb") as file:
        # Command for Uploading the file "STOR filename"
        ftp_server.storbinary(f"STOR {filename}", file)

async def main():
    topics = [
        pubsub.channel_points(users_oauth_token)[users_channel_id]
    ]
    await client.pubsub.subscribe_topics(topics)
    print("\n\nСкрипт успешно работает!\n")
    await client.start()

client.loop.run_until_complete(main())