#!/usr/bin/python3
#Script to bridge ERMA to discord. Make sure ERMA is running with BRIDGE_ACTIVE set to True

import os
import discord
import time
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents().all()
client = commands.Bot(command_prefix=',', intents=intents)

def string_save(filename, input):
    """Function to save a string to a file.
    Takes in an INPUT (string), and overwrites to FILENAME (string)"""
    with open(filename, "w") as file:
        file.write(input)

def string_read(filename):
    """Function to read a file.
    Takes inFILENAME (string) to open and read."""
    with open(filename, "r") as read:
        return read.read().rstrip() #rstrip removes the extra newline at the end

def start(discord_bot_token, triggers, ai_file, user_file):
    """Function to start the discord bot portion.
    DISCORD_BOT_TOKEN is the discord bot token, and should be a string.
    TRIGGERS is the list of trigger phrases, and should be a list of strings"""
    @client.event
    async def on_ready():
        print('online')
    @client.event
    async def on_message(message):
        if message.author == client.user or message.author.bot:
            return
        for i in range(len(triggers)):
            if triggers[i].lower() in message.content.lower():
                if os.path.isfile('summarize'): #if the model is summarizing, we don't want to interrupt it
                    return await message.channel.send("Model is summarizing. Please try again later.")
                string_save(ai_file, "") #otherwise, we first blank out the previous outputs...
                print('User input received!')
                string_save(user_file, message.content) #...then write to USER_FILE, triggers ERMA to continue
                while True:
                    ai_read=string_read(ai_file) #store this first
                    if ai_read != "": #when ai_file is repopulated, that means AI has sent out its stuff
                        print('AI response sent!')
                        string_save(ai_file, "") #now blank it
                        return await message.channel.send(ai_read)
                    else: #AI is not ready to send out
                        if os.path.isfile('summarize'):
                            print("Summarization in progress...")
                            return await message.channel.send("Model is summarizing. Please try again later.") #stop, we don't want to interrupt it
                        time.sleep(2.0)
    client.run(discord_bot_token)

## Initialize script using the template below. Change TRIGGERS as you want. ##
#start(os.getenv('DISCORD_API_KEY'), ["hey gpt"], "neuralcloud_ai.file", "neuralcloud_user.file")