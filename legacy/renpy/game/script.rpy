# The script of the game goes in this file.
# Hurr Durr inefficient programming hours!

# This renpy scripts.rpy works hand in hand with backend.py. Make sure that is started first.
# Required files for integration:
    # toggle
    # modelInput
    # modelOutput
    # sentiment

#Set renpy defaults
default preferences.afm_enable = False
default preferences.desktop_rollback_side = "disable" #disable back button
default preferences.mobile_rollback_side = "disable" #disable back button
default true = True
image gpt neutral = "neutral.png"
image gpt positive = "positive.png"
image gpt negative = "negative.png"

# The game starts here. It's really not a game, but just a hacky way to give a GUI to an api.
label start:
    scene bg
    show gpt neutral #base sentiment so we don't start on an empty screen or something
    while true:
        python: #This reads off of the toggle file shared between renpy and the backend.py.
            f = open(renpy.loader.transfn("bridge/toggle"),"r")
            toggle = f.read()

        if toggle == "output": #If the toggle has content output, then we have renpy fetch the model's latest output and show it.
            #begin python scripting
            python:
                sentAnalysis = open(renpy.loader.transfn("bridge/sentiment"),"r") #This tells renpy to read contents of file sentiment, so it can display character expressions.
                sentiment = sentAnalysis.read()
                if "positive" in sentiment.lower(): #positive is set to 1, which will point to positive character image
                    sentiment = 1
                elif "negative" in sentiment.lower(): #negative is set to 2, which will point to negative character image
                    sentiment = 2
                elif "neutral" in sentiment.lower(): #neutral is 0, which points to neutral character image
                    sentiment = 0
                else: #catch-all in case the api does something funky.
                    sentiment = 0

                modelOutput = open(renpy.loader.transfn("bridge/modelOutput"),"r") #This tells renpy to read contents of file modelOutput, which contains the output of the model.
                text = modelOutput.read()

                toggleChanger = open(renpy.loader.transfn("bridge/toggle"), "w+")
                toggleChanger.write(text) #By writing something random, we can allow the backend to proceed with its script.
                toggleChanger.close()

            #begin renpy conditionals. Im sure theres a way to get this into python itself, but i cant get it working. so it goes    
            if sentiment == 1:
                show gpt positive 
            elif sentiment == 2:
                show gpt negative 
            elif sentiment == 0:
                show gpt neutral

            python: #actual showing dialog.
                list=text.split() #this splits the output text into a list of words.
                n = 40 
                out=[list[i:i+n] for i in range(0, len(list), n)] #splits lists into smaller lists of n or less words. refer to previous line for n
                for x in range(len(out)):
                    string = ' '.join(out[x]) #convert list back to string with space delimiter
                    renpy.say("", string)

        elif toggle == "input": #If the toggle has content input, then we have renpy ask user for input, so that backend can read off its file later.
            show gpt neutral
            python:
                input = renpy.input("Enter your input: ")
                modelInput = open(renpy.loader.transfn("bridge/modelInput"), "w+")
                modelInput.write(input) #this writes the user input to a file cleverly named modelInput
                modelInput.close()
                
                toggleChanger = open(renpy.loader.transfn("bridge/toggle"), "w+")
                toggleChanger.write(input) #By writing something random, we can allow the backend to proceed with its script.
                toggleChanger.close()

        else:
            pause 0.5 #just keep iterating through this loop until one of the other conditions get triggered.
    return