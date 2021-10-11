from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from discord.ext import commands, tasks
import discord, os, socket, datetime, json, time

from urllib import parse, request
import re

#ch={38: {'name': 'MAC', 'solved': False},37: {'name': 'L33k', 'solved': True},36: {'name': 'shshshsh', 'solved': True},35: {'name': 'eLearning', 'solved': True},10: {'name': 'Invincible', 'solved': True},20: {'name': 'Welcome', 'solved': True}, 5: {'name': 'Leaky Blinders', 'solved': True}, 14: {'name': 'Chhili', 'solved': True}, 3: {'name': 'Crypt', 'solved': True}, 4: {'name': 'listening?', 'solved': True}, 26: {'name': 'Notes', 'solved': True}, 24: {'name': 'Blacklist Revenge', 'solved': True}, 17: {'name': 'Saw', 'solved': True}, 18: {'name': 'Time Machine', 'solved': True}, 27: {'name': 'SeoFtw', 'solved': True}, 6: {'name': 'Transfer', 'solved': True}, 8: {'name': 'Login', 'solved': True}, 9: {'name': 'Boombastic', 'solved': True}, 12: {'name': 'Procyon', 'solved': True}, 13: {'name': 'New Employee', 'solved': False}, 19: {'name': 'OP NUMBER STATION', 'solved': True}, 21: {'name': 'Shisui', 'solved': True}, 22: {'name': 'Containers?', 'solved': True}, 28: {'name': 'BF', 'solved': True}, 29: {'name': 'Omen', 'solved': True}, 30: {'name': 'Peaky &amp; the Brain', 'solved': True}, 32: {'name': 'Sora', 'solved': False}, 33: {'name': 'ParrotOx', 'solved': True}, 34: {'name': 'devprivops', 'solved': True}}
bot = commands.Bot(command_prefix='>', description="Znfl is at your disposal :sunglasses:")

#commands
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

#@bot.command(name = 'listCommands', aliases = ['List', 'list'])
#async def listCommands(ctx):

@bot.command()
async def flag(ctx):
    await ctx.send("Noooo not here the good stuff is a secret :shushing_face: \nhit me up in my dms(message the bot privately)")

@bot.command()
async def socials(ctx):
    embed = discord.Embed(title=f"Fword", description="Fword team social media", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Website", value=f"https://www.fword.tech/")
    embed.add_field(name="Facebook", value=f"https://www.facebook.com/fwordteam/")
    embed.add_field(name="Twitter", value=f"https://twitter.com/FwordTeam")
    embed.set_thumbnail(url="https://i.imgur.com/Qi6NI0E.png")

    await ctx.send(embed=embed)


# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(url="https://fword.tech/"))
    print('The Bot is Ready')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    usernameStr = '###CTFd_CREDS###'
    passwordStr = '###CTFd_CREDS###'

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options )

    print('loading')
    browser.get(('https://ctf.fword.tech/login'))
    print('loaded')
    time.sleep(20)
    username = browser.find_element_by_id('name')
    username.send_keys(usernameStr)
    password = browser.find_element_by_id('password')
    password.send_keys(passwordStr)

    submitBtn = browser.find_element_by_class_name('btn')
    submitBtn.click()
    browser.get(f'https://ctf.fword.tech/api/v1/challenges')
    html = browser.page_source
    time.sleep(2)
    html = html[html.index('{'):html.rindex('}')+1]
    y = json.loads(html)
    for i in range(len(y['data'])):
        ch[y['data'][i]['id']] = {'name':y['data'][i]['name'],'solved': False}
    print(ch)
    await firstBlood.start()


@bot.listen()
async def on_message(message):
    if "flag" == message.content.lower():
        try:
            if message.channel.id == message.author.dm_channel.id:
                #await message.channel.send('**THE CTF HASN\'t STARTED YET**')
                await message.channel.send('**HAVE FUN**\nFwordCTF{Welcome_To_FwordCTF_2021}')
                await bot.process_commands(message)
        except:
            pass

#tasks
@tasks.loop(seconds=180)
async def firstBlood():

    allSolved = True
    keys = dict.keys(ch)
    for i in keys:
        if not(ch[i]['solved']):
            allSolved = False

    if(allSolved):
        return
    
    channel = bot.get_channel(int('###CHANNEL_ID###'))

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    usernameStr = '###CTFd_CREDS###'
    passwordStr = '###CTFd_CREDS###'

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options )

    print('loading')
    browser.get(('https://ctf.fword.tech/login'))
    print('loaded')

    username = browser.find_element_by_id('name')
    username.send_keys(usernameStr)
    password = browser.find_element_by_id('password')
    password.send_keys(passwordStr)

    submitBtn = browser.find_element_by_class_name('btn')
    submitBtn.click()


    for i in keys:
        
        if(ch[i]['solved']):
            continue

        browser.get(f'https://ctf.fword.tech/api/v1/challenges/{i}/solves')
        html = browser.page_source
        time.sleep(2)
        html = html[html.index('{'):html.rindex('}')+1]
        y = json.loads(html)
            
        try: y['data']
        except:
            print('key error')
            continue

        if(y['data']==[]):
            continue

        if(y['data']==[]):
            print(f'no data for {ch[i]}')
            continue

        ch[i]['solved'] = True
        # print(f'`First blood for challenge: {ch[i]["name"]} goes to {y["data"][0]["name"]}`')
        print("sending")
        await channel.send(f'```css\n🩸 First blood for .{ch[i]["name"]} goes to [{y["data"][0]["name"]}]```')
        print(ch)
    browser.close()
    print('Completed!')



bot.run('###BOT_KEY###')