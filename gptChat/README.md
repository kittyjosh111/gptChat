Ok so, this is an interesting script in that I know its really inefficient and redundant, but it seems to work for what it was designed for. Unfortunately, this also means I will forget the pathways I built to get this working. It also means its going to be really troublesome for someone to read the code and know what I'm doing. So while the memory is still fresh, lets try explaining this again.

Renpy is not pure python. That means I can't really stick my entire gpt script from my repo into renpy and have it work. What I thought then was to run the gpt script as a "backend" or server for renpy to read off of. The files shared between renpy and this ```backend.py``` thus have to be somewhere accessible. Thus, ```backend.py``` and the files it generates ```neuralcloud_renpy.ncb``` ```log_renpy.log``` are found in the folder ```game/bridge```. 

Cool. So the gpt scripts I wrote earlier can in fact still be used. How do we connect renpy to all of this?

Renpy is able to read and write files by using python in its script. Let's use that to our advantage.

The original gpt scripts required user input. This came in the form of typing into a terminal, or through discord intents. We don't have either now, but Renpy has a function to request input from the player. Then, we need a bridge between the renpy user input and the gpt script. 

This brings up the need for three things:

1) I need to edit the input part of the main function in ```backend.py```
2) There needs to exist some file that tells renpy whether to ask for input or display ```backend.py```'s api request outputs
3) There needs to exist some file that renpy can write the user input so that ```backend.py``` can read from and send out to OpenAI.

Number 1 is achieved by editing the ```backend.py```. Number 2 is achieved by creating the ```toggle``` file in the bridge folder. Writing the word "input" to it makes the renpy script prompt user for input, which is then written to ```modelInput```, which solves number 3.

So far, we have ```toggle``` controlling what renpy does, and ```modelInput``` that allows renpy to bridge the user input to the ```backend.py```

Then, when we have the model give its output, there needs to be a way to 

1) Tell renpy to look for said output
2) Have renpy read said output and display for user to see.

Number 1 is achieved by editing ```toggle``` so that its contents read "output". Then, renpy is triggered to read from a file ```modelOutput```, which was created by ```backend.py```, and contains the output from the api request. Neat.

Now, so far, we have ```toggle``` controlling what renpy does, ```modelInput``` that allows renpy to bridge the user input to the ```backend.py```, and ```modelOutput``` that allows ```backend.py``` to bridge the api response to renpy.

Cool. So now we have the bridging working. However, there needs to be a way to have both scripts pause themselves when waiting for the other one to finish modifying the aforementioned values. 

For ```backend.py```, we can achieve this by looking at the last modified date of ```toggle```. If there hasn't been changes to that file, then it will pause the script, waiting for renpy to finish (user interaction). Then, renpy can **modify ```toggle``` in any way** and this triggers ```backend.py``` to continue with the script. Thus, a simple way for ```backend.py``` to wait for renpy is implemented.

For renpy, we can use ```toggle``` again to have it wait. Since a value of "output" in ```toggle``` tells renpy to display the api response, and a valuie of "input" tells renpy to ask for user input, then having an ```else:``` statement in the script controls whenever this is not the case. Having renpy then sleep creates a loop where renpy won't do antyhing but continuously check whether ```toggle``` finally contains a value of either output or input.