"""Just to be very clear, I really don't know how to use renpy.

The script of the game goes in this file.

** erma.py should be started first and configured BEFORE running this renpy project. **
** sentiment.py should be started first and configured BEFORE running this renpy project. **
** if sentiment.py is not run, you WILL NOT see different emotions on the images **

The first check is whether 'summarize' exists. If it does, we wait for it to go away.
 Then we check whether user_file has any contents. If it doesn't, we know it is the user's turn,
   and thus we have renpy ask for the user's input.
 Else, we know it is the AI's turn and they might be busy generating input.
   thus, we wait until ai_file is next modified (erma writes the AI output to ai_file), then have 
   renpy read and display the contents of ai_file. During this process, user_file should have been
   blanked out, thus we are ready for the next cycle.
 Additionally, we check for the 'sentiment' file to be filled before displaying ai output. If it is
 non-existent, we don't change the image shown through Ren'Py"""

# Define the images to use
image gpt neutral = "neutral.png"
image gpt positive = "positive.png"
image gpt negative = "negative.png"

# Python time:
init python:

    import os
    import time

    # First define these vars
    ai_file = "neuralcloud_ai.file"
    user_file = "neuralcloud_user.file"

    # Then the functions
    def string_read(filename):
        """Function to read a string from a file.
        Takes in an FILENAME (string) and returns contents"""
        return open(filename,"r").read()

    def string_save(filename, input):
        """Function to save a string to a file.
        Takes in an INPUT (string), and overwrites to FILENAME (string)"""
        return open(filename, "w+").write(input)

    def exists(filename):
        """Function that checks if the FILENAME is detected by Ren'Py.
        It is just a try except wrapper that returns either the FILENAME path or False"""
        try:
            return renpy.loader.transfn(filename)
        except:
            return False

    def wait_modified(filename):
        """Function that looks at the time at which a FILENAME (string) was last edited.
        If that time changes, it means FILENAME was edited, and we return its new contents."""
        last_modified = os.path.getmtime(filename)
        while last_modified == os.path.getmtime(filename):
            time.sleep(2.0) #adjust as necessary as to not burn out your processor
        else:
            return string_read(filename)

    def splitter(text, split):
        """Function to split a large block of text TEXT
        into smaller chunks length SPLIT"""
        text_split = text.split()
        for each in range((len(text_split) // split) + 1):
            renpy.say("", ' '.join(text_split[:split])) #put it back together
            text_split = text_split[split:] #reassign the original list
        return

    ai_file = exists(ai_file) #now we make sure renpy can easily read/write these files...
    user_file = exists(user_file)
    summarize_toggle = exists('summarize') #there are no user options to change this name
    sentiment = exists('sentiment') #same here

# Set renpy defaults
default preferences.afm_enable = False
default preferences.desktop_rollback_side = "disable" #disable back button
default preferences.mobile_rollback_side = "disable" #disable back button

# The game starts here.
label start:
    scene bg #this loads in the bg.* file in the images directory
    show gpt neutral #base sentiment
    # These display lines of dialogue.
    # Nuh uh! Infinite loops!
    while True:
        while summarize_toggle:
            pause 2 #just keep iterating through this loop
            $ summarize_toggle = exists('summarize') #then update it
        python:
            if not string_read(user_file): #user_file will be blanked by erma once it is passed to the AI
                user_input = renpy.input("Enter your input: ")
                string_save(user_file, user_input)
            else: #must be AI turn
                def wait_splitter(text, split, sent_file):
                    """Function to call SPLITTER() on TEXT and SPLIT once
                    SENT_FILE has been modified"""
                    text_out = text
                    sent_out = wait_modified(sent_file)
                    if 'positive' in sent_out:
                        renpy.show('positive')
                    elif 'negative' in sent_out:
                        renpy.show('negative')
                    else: #neutral and other edge cases
                        renpy.show('neutral')
                    string_save(sentiment, "") #blank this out
                    return splitter(text_out, 32) #run the other one
                if sentiment:
                    wait_splitter(wait_modified(ai_file), 32, sentiment) #run
                else:
                    splitter(wait_modified(ai_file), 32) #run without sentiment
        pause 0.5
    # This ends the game. I don't think we ever reach here.
    return
