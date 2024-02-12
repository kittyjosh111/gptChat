# gptChat

---

### Intro:

Simple scripts to mimic a chat function using OpenAI's api. Note that you will need an OpenAI API to run this.

These scripts in the enhancedMemory folder work similarly to those found in the cli folder, but differ in that they actively compress the memory of the model after a set number of interactions, attempting to prolong the "life" of a model.

### Setup:

I recommend running these scripts in a virtual environment. I'll assume you know how to set one up and activate it. If not, refer to the docs: https://docs.python.org/3/library/venv.html

First use pip to install the ```requirements.txt```, then you can open a script in a text editor to tweak the variable values to your liking.

Find ```limit_length=50```. This means that the script will summarize the model's ncb every 50 lines of dialogue including both you and the model. Change this if you want. The higher the number, the less frequent the summarization, and the lower, the more frequent.

### Logic behind my scripts:

Refer to the logic in the cli scripts, as this is nearly the same. The difference comes down to the following:

This script under attempts to prolong the "life" a script can offer by summarizing past conversations into a brief sentence every 50 or so exhanges of dialogue. This summary overwrites the ncb file, and requires the log and ncb to be in sync. A backup of both the ncb and the log is created every time the summary is performed, in case you want to restore it.

The summary output is added to the system content of the chatGPT api, thus it should adhere to the general gist of your previous conversations.
