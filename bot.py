import discord
import shlex
import yaml
import urllib.request
import re
import os
import sys

import reaction

# get token
try:
    with open('auth.yaml', 'r') as f:
        auth = yaml.load(f)
        if 'token' in auth:
            TOKEN = auth['token']
        else:
            print('Error parsing auth.yaml')
            sys.exit(1)
except:
    print('Error opening auth.yaml')
    sys.exit(1)


client = discord.Client()

PREFIX = '!'

# run bot command
async def run_command(message):
    if message.author == client.user:
        return

    # process arguments
    try:
        argv = shlex.split(message.content[1:])
    except ValueError:
        await client.send_message(message.channel, 'Error: could not parse input')
        return

    command = argv[0].lower()

    if command == 'r' or command == 'react':
        await reaction.do_react(client, message, argv)
    elif command == 'l' or command == 'list':
        await reaction.do_list(client, message, argv)
    elif command == 'a'or command == 'add':
        await reaction.do_add_react(client, message, argv)
    elif command == 'd' or command == 'delete':
        await reaction.do_remove_react(client, message, argv)
    elif command == 'h' or command == 'help':
        await do_help(client, message, argv)
    else:
        await do_unknown(message, argv)

# show help message
async def do_help(message, argv):
    msg = gen_help()
    await client.send_message(message.channel, msg)


# unknown command
async def do_unknown(message, argv):
    msg = 'Sorry, I don\'t understand that command\n'
    msg += gen_help()
    await client.send_message(message.channel, msg)


# generate help text
def gen_help():
    msg = 'list of commands:\n'
    msg += '**Reply with a reaction**\n'
    msg += '`{}react reaction`\n'.format(PREFIX)
    msg += 'Example: `{}react bang`\n'.format(PREFIX)
    msg += '\n**Add a new reaction**\n'
    msg += '`{}add reaction_command message_text link_to_file`\n'.format(PREFIX)
    msg += 'Example: `{}add bang "Bang bang bang!" example.com/bang.gif`\n'.format(PREFIX)
    msg += '\n**Delete a reaction**\n'
    msg += '`{}delete reaction_command`\n'.format(PREFIX)
    msg += 'Example: `{}delete bang`\n'.format(PREFIX)
    msg += '\n**List all reactions**\n'
    msg += '`{}list`\n'.format(PREFIX)
    return msg


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(PREFIX):
        await run_command(message)
        return



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
