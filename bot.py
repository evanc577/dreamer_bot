import discord
import shlex
import yaml
import sys

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
    # process arguments
    try:
        argv = shlex.split(message.content[1:])
    except ValueError:
        await client.send_message(message.channel, 'Error: could not parse input')
        return

    if argv[0].lower() == 'r':
        await do_react(message, argv)
    elif argv[0].lower() == 'react':
        await do_react(message, argv)
    elif argv[0].lower() == 'l':
        await do_list(message, argv)
    elif argv[0].lower() == 'list':
        await do_list(message, argv)
    elif argv[0].lower() == 'h':
        await do_help(message, argv)
    elif argv[0].lower() == 'help':
        await do_help(message, argv)
    else:
        await do_unknown(message, argv)


# reply with a messange and file
async def do_react(message, argv):
    if len(argv) != 2:
        msg = 'Error: needs 1 argument. See `$help`'
        await client.send_message(message.channel, msg)
        return

    # read replies from file
    try:
        with open('replies.yaml', 'r') as f:
            replies = yaml.load(f)
    except:
        print('Error opening replies file')
        return

    # respond with reply
    if argv[1] in replies:
        msg = replies[argv[1]]['message']
        f = replies[argv[1]]['file']
        await client.send_file(message.channel, f, content=msg)
        return
    else:
        await client.send_message(message.channel, 'That reaction doesn\'t exist! :\'(')
        return


# list current reactions
async def do_list(message, argv):
    # read replies from file
    try:
        with open('replies.yaml', 'r') as f:
            replies = yaml.load(f)
    except:
        print('Error opening replies file')
        return

    msg = 'Here are my current reactions!\n```\n'
    for k in sorted(replies):
        msg += k + '\n'

    msg += '```'
    await client.send_message(message.channel, msg)
    return


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
