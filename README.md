<img src = "./insta-bot.png" width="100%">

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

# Instagram-Bot<img src="https://pngimage.net/wp-content/uploads/2018/06/icono-instagram-peque%C3%B1o-png-3.png" width="3.5%"/><img src="https://i.pinimg.com/originals/f6/d7/ef/f6d7ef4b5b015be7cf607e2087c0a244.png" width="3%"/>

### ⚠️ Caution:

**Not meant for commercial or spamming purposes, created for educational and learning purpose only.**

### _Check releases section for downloadable single executable file._

## Steps to Create a Release (.exe) using PyInstaller: :footprints:

1. Run `pip install pyinstaller` to install Pyinstaller.
2. Run the following command to create a the build (.exe) :  
   `pyinstaller ./main.py --onefile --icon=favicon.ico --add-binary "./driver/chromedriver.exe;./driver"`
3. This creates 2 directories namely _build_ and _dist_.
4. Go to _dist_ and open main.exe.

## Steps to Run Locally (Tested on Python 3.6) :footprints:

1. Clone the repo.
2. Navigate to the cloned directory.
3. Create a virtual environment, for the current project by running the following command `py -m venv env`.
4. Then install all the required libraries by running `pip install -r requirements.txt`.
5. Download and Extract the chromedriver.exe in the _driver_ folder. Download from [here](https://chromedriver.chromium.org/downloads) depending on your OS.
6. Add a credentials.py file, within it declare two variables with **username_1** and **password_1**.
7. Now run the **main.py** file using `python main.py`.
8. Following is the description of functions.

## GUI has been added for Client Friendly Interface

## Bot Functions: :robot:

The functions of the bot are pretty straight-forward till now. This bot uses **selenium** to automate Google Chrome to perform it's tasks. The functions include:

1. List of Followers
2. List of Following
3. List of Unfollowing
4. List of Blue-Tick Following
5. Unfollow the Unfollowers based on count.
6. Retain information of the user handles unfollowed.
7. Follow users based on count.

## What's coming more? :thinking:

AI powered comments on images. (Help Needed)

### Have Suggestions or if you would want to contribute, just add a PR (Tests to be added soon.)

Created with ❤️ by Tarun.
