import discord
import yaml
import sys
from datetime import datetime, time, timezone
from time import sleep
from threading import Thread, Lock

# get token
try:
    with open('auth.yaml', 'r') as f:
        auth = yaml.safe_load(f)
        if 'token' in auth:
            TOKEN = auth['token']
        else:
            print('Error parsing auth.yaml')
            sys.exit(1)
except:
    print('Error opening auth.yaml')
    sys.exit(1)

client = discord.Client()
mutex = Lock()

@client.event
async def on_ready():
    mutex.acquire()

    try:
        with open('messages.yaml', 'r') as f:
            messages = yaml.safe_load(f)
    except:
        print('Error opening messages.yaml')
        sys.exit(1)

    message_channel = None

    for server in client.guilds:
        if server.id == messages['server']:
            for channel in server.channels:
                if channel.id == messages['channel']:
                    message_channel = channel
                    break

    if message_channel == None:
        print('Specified channel not found')
        sys.exit(1)

    for i in range(31, -1, -1):
        if i in messages['songs']:
            s = messages['songs'][i]
            if s['sent']:
                continue

            t = datetime.strptime(s['time'], '%Y-%m-%dT%H:%M:%S%z')
            m = f"**{i}: {s['song']}**\n{s['link']}\n*{s['blurb']}*"
            print(f"waiting until {str(t)}")

            while t > datetime.now(timezone.utc):
                sleep(1)

            await message_channel.send(m)
            messages['songs'][i]['sent'] = True

            with open('messages.yaml', 'w') as f:
                yaml.dump(messages, f)

    mutex.release()

client.run(TOKEN)
