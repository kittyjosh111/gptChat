# gptChat

---

### Intro:

Simple scripts to make a gpt-3.5-turbo powered discord bot.

### Setup:

I recommend running these scripts in a virtual environment. I'll assume you know how to set one up and activate it. If not, refer to the docs: https://docs.python.org/3/library/venv.html

First use pip to install the ```requirements.txt```, then you can open a script in a text editor to tweak the variable values to your liking.

Then you can put your API key into the top of the script, where ```openai.api_key = ""``` is. Run the script with cli or gui, whichever you know how. To stop, just kill the script with ^C.

Put your discord bot token in the quotes also in the top of the script.

### Logic behind my scripts:

Refer to the readme in the cli folder, as these function the same. The only difference is that this requires a discord bot token. Look online on how to make a bot and get its token. The bot needs all privileges (presence intent, content intent, etc) set on the developer page. Refer to any errors you get when running the script if you encouter them.

These scripts will make ```neuralcloud_discord.ncb``` and ```log_discord.log```.

```discord_chatGPT.py``` runs without compressing memory, so it is more prone to higher costs and hitting max_tokens. 

```beta.py``` uses the memory compression found in the scripts under enhancedMemory/.