# discord-erma

### Intro
Discord bridging services for ```erma.py```

### Setup
You are advised to run it in a virtual environment. Remember to ```pip install -r requirements.txt```

First, move ```discord-erma.py``` into the folder where ```erma.py``` is located.

Then edit ```.env``` to include your discord bot api token.

Then, start ```erma.py``` with ```bridge_active``` set to True. Refer to Erma's readme for more information. 

```discord-erma.py``` is currently meant to be run in an interactive mode: ```python3 -i XXX.py```. You can look at the last few lines for a hint on how to start up the script.

You should know what ```ai_file``` and ```user_file``` are if you ran ```erma.py```. Pass them into ```start()```.