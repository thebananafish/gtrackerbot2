# gFTP-BOT.py - gFTP-BOT modules

import re, os, subprocess, HTMLParser, feedparser

# Constants
regex =  re.compile(r'>Password:(.*?)<')
rs = re.compile(r'(.*?)')
dead = re.compile(r'(\(dead\))')
h = HTMLParser.HTMLParser()

commands = [
    ' ',
    'Username: ftp_username | Password: ftp_password | Server: server_IP | Port: 21',
    ' ',
    '.ftp-search allows you to search gFTP-BOT\'s file collection, '
    'for example .search *.pdf',
    '.uptime displays gFTP-BOT\'s current uptime',
    '.rs title searches rs.4chan.org and returns the results'
]

"""List gFTP-BOT's commands via PRIVMSG"""
def help(phenny, input):
    phenny.msg(input.nick, ' ')
    phenny.msg(input.nick, 'Welcome to gFTP-BOT\'s help list, ' + input.nick + '.')
    for command in commands:
        phenny.msg(input.nick, command)

help.commands = ['help']
help.priority = 'medium'

"""Searches the server for a specific file and returns the results"""
def ftpsearch(phenny, input):
    query = input.group(2)
    fileSize = 0

    if not query:
        return phenny.reply('.ftp-search title')

    p = subprocess.Popen('locate -l 20 ' + query, shell=True, stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

    """Returns the search results in private message to the user"""
    phenny.msg(input.nick, "Hello " + input.nick + "! I've found the following results for " + query + ".")
    phenny.msg(input.nick, " ")

    for line in p.stdout.readlines():
        """Return the file size in an appropriate format"""
        fileSize = os.stat(line.strip('\n')).st_size
        if fileSize <= 1024:
            fileSize = str(fileSize) + 'B'
        elif fileSize <= 1048576:
            fileSize = str(fileSize / 1024) + 'KiB'
        elif fileSize <= 1073741824:
            fileSize = str(fileSize / 1024**2) + 'MiB'
        else:
            fileSize = str(fileSize / 1024**3) + 'GiB'

        phenny.msg(input.nick, line + "      " + fileSize)

ftpsearch.commands = ['ftp-search']
ftpsearch.priority = 'high'
ftpsearch.example = '.ftp-search *.pdf'

"""Returns df -h /dev/sda2 - Will only work if the command
   is issued by the bot admin in PRIVMSG"""
def df(phenny, input):
    if input.sender.startswith('#'): return
    if input.admin:
        p = subprocess.Popen('df -h /dev/sda2', shell=True, stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
        for line in p.stdout.readlines():
            phenny.msg(input.nick, line)

df.commands = ['df']
df.priority = 'high'

"""Returns gFTP-BOT's uptime information to the channel"""
def uptime(phenny, input):
    if input.sender.startswith('#'):
        p = subprocess.Popen('uptime', shell=False, stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
        for line in p.stdout.readlines():
            phenny.reply("gFTP-BOT's uptime: " + line)

uptime.commands = ['uptime']
uptime.priority = 'low'

""" Display the search results in PRIVMSG to the user """
def results(phenny, input, title, link, password = False):
    if password:
        phenny.msg(input.nick, 'Title: ' + title)
        phenny.msg(input.nick, 'Link: '+ link)
        phenny.msg(input.nick, 'Password: ' +  h.unescape(password.group(1)))
    else:
        phenny.msg(input.nick, 'Title: ' + title)
        phenny.msg(input.nick, 'Link: ' + link)
    phenny.msg(input.nick, ' ')

""" Search rs.4chan.org and return the results in PRIVMSG """
def rs(phenny, input):

    if not input.group(2):
        return phenny.reply('.rs title')

    title = input.group(2).strip().replace(' ', '+')
    title = 'http://rs.4chan.org/?s=' + title + "&rss=1"
    d = feedparser.parse(title)
    
    """ Return the top 20 search results """
    for n in range(0,19):
        try:
            title = d.entries[n]['title']
        except IndexError:
            return
        link = d.entries[n]['link']
        deadlink = re.search(dead, d.entries[n]['description'])
        password = re.search(regex, d.entries[n]['description'])
        if deadlink:
            break
        else:
            results(phenny, input, title, link, password)

rs.commands = ['rs']
rs.priority = 'high'
