# gptChat

### Intro:

Simple scripts to mimic a chat function using OpenAI's api and other fun things. Note that you will need an OpenAI API to run this. 

Alternatively, refer to the LocalAI documentation and you could have these scripts point to LocalAI instead of OpenAI with minor modifications.

### General Setup:

I recommend running these scripts in a virtual environment. I'll assume you know how to set one up and activate it. If not, refer to the docs: https://docs.python.org/3/library/venv.html

For all scripts, first use pip to install the ```requirements.txt```, then you can open a script in a text editor to tweak the variable values to your liking. Usually, that ends up being the api key, as well as temperature, prompt, delimiters, etc.

Refer to the individual folder READMEs for more specific instructions on how to load in the API keys, or how to even start the script.

### Types of scripts:

Refer to the folder names for the scripts described here.

- ```erma```: The latest generation. Features a persistent memory, which summarizes itself, and also the ability to selectively save conersation summaries into a "garden" for recall later on. Erma was designed to be run either standalone in a terminal, or as a server with integration to other services, such as discord.

- ```legacy```: The first generation of scripts. They are generally written poorly and not very efficient. They still do work but have not been updated for the most recent OpenAI pip module. Refer to the README in there for more details.

### Logic behind my scripts:

The basic logic is that the scripts is that they query the api for a response based off of some sort of input. To retain "memory", these scripts will create two files to store previous conversations. This could be something like a ```neuralcloud_backup.ncb``` (ncb for **n**eural **c**loud **b**ackup). This ncb is basically the chatbot's memory, and logs user inputs, API responses, and the summer garden in Erma's case. **To reset the model "personality", remove the ncb file and other files created by the script.** This applies to all models.

Again, refer to each individual README.md for more information.

Note the neural cloud backup files are generally not cross-compatible between the scripts.

---