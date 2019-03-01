import discord
import shlex
import yaml
import urllib.request
import re
import os
import sys

# reply with a messange and file
async def do_react(client, message, argv):
    if len(argv) != 2:
        msg = 'Error: needs 1 argument. See `{}help`'.format(PREFIX)
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
    if argv[1].lower() in replies:
        msg = replies[argv[1].lower()]['message']
        f = replies[argv[1].lower()]['file']
        await client.send_file(message.channel, f, content=msg)
        return
    else:
        await client.send_message(message.channel, 'That reaction doesn\'t exist! :\'(')
        return


# add another reaction image
async def do_add_react(client, message, argv):
    if len(argv) != 4:
        msg = 'Error: needs 3 arguments. See `{}help`'.format(PREFIX)
        await client.send_message(message.channel, msg)
        return

    # only accept reaction commands <= 16 chars
    if len(argv[1]) > 16:
        msg = 'Error: reaction command must be <= 16 characters'
        await client.send_message(message.channel, msg)
        return

    # only accept alphanumeric+_ in reaction
    if not re.match(r'^\w+$', argv[1]):
        msg = 'Error: reaction command must only contain alphanumeric and \'_\' characters'
        await client.send_message(message.channel, msg)
        return

    # check if reaction command already exists
    try:
        with open('replies.yaml', 'r') as f:
            replies = yaml.load(f)
    except:
        print('Error opening replies file')
        return
    if argv[1].lower() in replies:
        msg = 'Error: reaction command `{}` already exists'.format(argv[1])
        await client.send_message(message.channel, msg)
        return

    # get image header
    try:
        d = urllib.request.urlopen(argv[3])
    except:
        msg = 'Error: could not open url `{}`'.format(argv[3])
        await client.send_message(message.channel, msg)
        return

    # check file type
    valid_types = ['image/gif', 'image/jpg', 'image/jpeg', 'image/png', 'image/webm', 'video/webm', 'video/mp4']
    if d.info()['Content-Type'] not in valid_types:
        msg = 'Error: file must be one of: {},\nfile is type {}'.format(valid_types, d.info()['Content-Type'])
        await client.send_message(message.channel, msg)
        return

    # check file size
    size_lim_MB = 5
    size_limit = size_lim_MB*1048576
    if int(d.info()['Content-Length']) > size_limit:
        msg = 'Error: file size must be < {} MB'.format(size_lim_MB)
        msg += '\nfile is {} B'.format(d.info()['Content-Length'])
        await client.send_message(message.channel, msg)

    # extract extension and download file
    f_ext = d.info()['Content-Type'].split('/')[1]
    f_path = './reply_files/{}.{}'.format(argv[1].lower(), f_ext)
    urllib.request.urlretrieve(argv[3], f_path)

    # update replies.yaml
    new_data = { argv[1].lower(): { 'message': argv[2], 'file': f_path } }
    try:
        with open('replies.yaml', 'r') as f:
            cur_yaml = yaml.load(f)
            cur_yaml.update(new_data)
    except:
        print('Error opening replies file')
        return
    try:
        with open('replies.yaml', 'w') as f:
            yaml.safe_dump(cur_yaml, f, default_flow_style=False)
    except:
        print('Error saving replies file')
        return

    # success!
    msg = 'Successfully added reaction `{}`'.format(argv[1])
    await client.send_message(message.channel, msg)

async def do_remove_react(client, message, argv):
    if len(argv) != 2:
        msg = 'Error: needs 1 arguments. See `{}help`'.format(PREFIX)
        await client.send_message(message.channel, msg)
        return

    # check if reaction command already exists
    try:
        with open('replies.yaml', 'r') as f:
            replies = yaml.load(f)
    except:
        print('Error opening replies file')
        return
    if argv[1].lower() not in replies:
        msg = 'Error: reaction command `{}` does not exist'.format(argv[1])
        await client.send_message(message.channel, msg)
        return

    #load file and remove react from it, then resave it
    try:
        with open('replies.yaml', 'r') as f:
            cur_yaml = yaml.load(f)
            # remove from local machine
            os.remove(replies[argv[1].lower()]['file'])
            #del from list
            del cur_yaml[argv[1].lower()]
    except:
        print('Error opening replies file')
        return
    try:
        with open('replies.yaml', 'w') as f:
            yaml.safe_dump(cur_yaml, f, default_flow_style=False)
    except:
        print('Error saving replies file')
        return

    # success!
    msg = 'Successfully removed reaction `{}`'.format(argv[1])
    await client.send_message(message.channel, msg)


# list current reactions
async def do_list(client, message, argv):
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


