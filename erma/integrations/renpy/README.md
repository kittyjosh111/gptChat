# erma renpy integration

### Intro
Ren'Py bridging services for ```erma.py```

### Setup

## Install: Using Ollama as the backend

1. Install Ollama and download an AI model. Follow the directions on their website.

2. Download the Ren'Py zip provided for your OS from this folder. These were created by building an empty project using the Ren'Py SDK. Don't trust me? You can do the same by downloading the Ren'Py SDK yourself. Then create a new project. Here you can even customize the project color theme. Then build it for your distribution. You'll get a zip file like the ones provided.

3. Unzip the zip file in the directory you want to run this project in.

4. Download the ```game``` folder from this repository.

5. Move the ```game``` folder into the unzipped Ren'Py project. Your computer should ask you whether you want to replace ```script.rpy```. Replace it.

6. Download this entire folder: https://github.com/kittyjosh111/gptChat/tree/main/erma

7. Move the contents of the folder EXCEPT integrations/ from the above step into game/erma/ inside your Ren'Py project.

8. Take a moment to look at your Ren'Py project folder. First look for ```launcher_services.py``` and ```script.rpy``` in the game/ folder. Now, inside the game/erma/ folder, you should see the following required files: ```erma.py```, ```sentiment.py```, and ```requirements.txt```. Other files are optional. You SHOULD NOT have the integrations folder in here.

9. Take a moment to edit ```erma.py```. First, replace the line: ```client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))``` with this instead: ```client = OpenAI(base_url = 'http://localhost:11434/v1', api_key='ollama')```. If hosting the ollama server elsewhere, tweak base_url to your needs.

10. Now uncomment the line ```ncb, ai_file, user_file = "neuralcloud_backup.ncb", 'neuralcloud_ai.file', 'neuralcloud_user.file'```. This should be near fourth to last line.

11. Then write the start function. MAKE SURE YOU SET BRIDGE_ACTIVE TO TRUE. As an example, you paste this function call into the last line of ```erma.py```: ```start('llama3', bridge_active=True, local_summary="philschmid/flan-t5-base-samsum")```. Replace llama3 with your model name. If you don't want to use the local_summary feature, remove that argument from inside the function call. Save changes and exit the file.

12. Make a python venv as to not clog your system python with random dependencies. I suggest creating this inside the game/ folder of the Ren'Py project. Wherever you make it, remember the filepath because we will use it later to run ```erma.py``` or other scripts. If you need an example command, you can run ```python3 -m venv venv``` to create the venv. Then activate it with ```source venv/bin/activate```.

13. Navigate to the game/erma/ folder of your RenPy project. In the venv from the previous step, install the requirements for ```erma.py``` with pip, using the ```requirements.txt```. For example, run ```pip install -r requirements.txt```.

14. Make sure that transformers is installed. Run ```pip install transformers```.

15. Navigate to or create the game/images/ folder in the RenPy project.

16. Put in three images, one for positive, neutral, and negative emotions. Title them ```positive.png```, ```neutral.png```, and ```negative.png```, respectively.

17. If you want, place a background image in the same folder and title it ```bg```. The file extension does not matter.

## Setting up backends with or without sentiment analysis

1. In a terminal window or however you usually run python files, activate the venv you created in step 12 from the installation.

2. Navigate to and run ```erma.py``` in the game/erma/ folder of your Ren'Py project. For example, ```python3 game/erma/erma.py```. Follow the instructions as they appear. You are done when the console reports something like "Starting conversaton". Once this appears, feel free to close the script.

3. If you DO NOT want sentiment analysis, feel free to skip this step and move on to the section labeled "Running the Ren'Py project WITHOUT sentiment analysis". Otherwise, open another window and repeat step 1. Navigate to ```sentiment.py``` in the game/erma/ folder of your Ren'Py project. Run it and allow the model to download. Once the console reports something like "Waiting for ai input", feel free to close the script.

## Running the Ren'Py project with sentiment analysis

1. Activate the python venv from step 12 of the installation. Then **in this venv**, launch the Ren'Py project. You can do this from CLI or GUI, whichever you are fluent in. If you launch it through CLI, you'll see debug messages for ```erma.py``` and ```sentiment.py```

2. Now you should be able to converse with the AI model through RenPy. To close it, press quit in the Main Menu or settings screen.

## Running the Ren'Py project WITHOUT sentiment analysis

1. Open up ```script.rpy``` in the game/ folder of the Ren'Py project. Replace the line ```launcher_services.start()``` with ```launcher_services.start(sentiment=False)```.

2. Go to the game/erma/ folder in the Ren'Py project directory. If ```sentiment``` is there, delete it.

2. Activate the python venv from step 12 of the installation. Then **in this venv**, launch the Ren'Py project. You can do this from CLI or GUI, whichever you are fluent in. If you launch it through CLI, you'll see debug messages for ```erma.py```.

3. Now you should be able to converse with the AI model through RenPy. To close it, press quit in the Main Menu or settings screen.

## Running the Ren'Py project manually with CLI

1. Open up ```script.rpy``` in the game/ folder of the Ren'Py project. Comment out the line ```launcher_services.start()```. Save and exit.

2. Open a terminal window. Activate the python venv from step 12 of the installation. Then **in this venv**, navigate to ```erma.py``` in the /game/erma/ folder. Launch it with something like ```python3 erma.py```. Do not close this window, it is the 'brains' of this project.

3. If you DO NOT want sentiment analysis, feel free to skip to the next step. Otherwise, open another window and repeat step 1-2. Navigate to ```sentiment.py``` in the game/erma/ folder of your Ren'Py project. Run it. Do not close this window, it is the 'heart' of this project.

4. In yet another terminal window, launch the Ren'Py project. You do not need to be in a venv for this step.

5. Now you should be able to converse with the AI model through RenPy. To close it, press quit in the Main Menu or settings screen. Then go back to all the terminal windows from the previous steps and exit those processes.