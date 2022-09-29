# MagellanEU4 
Magellan is a map editing software for EU4, aimed at helping players easily modify maps for EU4, particularly for full conversion mods.

## Setup:

Unfortunately for you non-programmers, there isn't a single executable (.exe) file you just need to download and run. Thus, the following steps are required

1. Download Python and the necessary Libraries

- Magellan uses a programming language called 'Python', which must be installed.
- This can be downloaded at https://www.python.org/downloads/. It is highly recommended to download the latest release
- Magellan also uses a few libraries not included in the base python installation. To download them run the following commands in your terminal: `pip install tk`, `pip install ttkwidgets`, `pip install PIL`, `pip install numpy`. If `pip` doesn't work, try `pip3`

2. Download Git and Navigate through the Command Line

- This tool is constantly in development. Thus, the best way to download all the files and keep them up to date is with Git
- First, download Git (if your computer doesn't already have it)
- Next, IN YOUR TERMINAL, navigate to the folder where you would like to download Magellan. Assuming you want the folder for the tool to reside in `C:\User\<YourUserName>\Documents` for example, input the command `cd C:\User\<YourUserName>\Documents`
- Afterwards, run the command `git clone https://github.com/Graapefruit/MagellanEU4.git`. This will automatically create a new folder inside your current directory with all the files for Magellan copied over!
- Enter this folder with `cd MagellanEU4`

3. Run/Updating Magellan

- Ensure that your terminal is in the correct directory. If you followed all the steps above, you should be good. Otherwise, or if you need to get back here, `cd C:\User\<YourUserName>\Documents\MagellanEU4` should do the trick
- Run the following command in your terminal: `python MagellanEU4.py` (It is recommended you run it this way through the terminal, rather than double-clicking on it in the File Explorer. This is because, if Magellan crashes with an error, you won't be able to see the error, and thus diagnose the problem)
- NOTE that python is... a little messy with packaging sometimes. If `python` doesn't work, try `py`, `py3`, or `python3`
- Since this tool is always in development, run `git pull` to automatically download any new changes since you last installed/updated it. 

## How to Use

1. Before doing anything, since this tool is still in development, I *HIGHLY HIGHLY HIGHLY RECOMMEND KEEPING A BACKUP OF YOUR MOD SOMEWHERE*. Magellan writes all changes directly to your mod folder. In case it bugs out, some of your files might be overwritten with incorrect or corrupted data. Thus, *KEEP A BACKUP OF YOUR MOD*. I personally use GitHub for my mod(s), which I highly recommend you look into using, if you don't already.
1. Start by loading your mod. Use File->Open, and navigate to wherever your mod is. This was in `C:\Users\<YourUserName>\Documents\Paradox Interactive\Europa Universalis IV\mod\<YourModName>` on my window machine. Magellan reads a lot of files, and it will let you know if any Necessary/Optional ones are missing.
2. Once the map loads... start editing your map! Click on a province to edit any of it's data. 
3. Use the MapModes at the top to see your map in a different mode. very similar to how it works in EU4. While viewing a mapmode that isn't the default provinces mapmode, you can right-click to copy the data key to your current mapmode from your currently selected province to another province you right-click on. (For example: load the religion mapmode. Select Rome. Right click on Jerusalem. Congrats, Jerusalem is now catholic, and you did in 3 seconds what the crusaders failed to do over the course of multiple centuries)
4. Tag-Editing is still not functioning and under construction. Stay tuned!
5. Whenever you're done, hit File->Save to save your changes. Look at the terminal once you do to see if there were any errors
6. Thats all!

## Last Notes

Magellan is a great tool, and to be honest with the nature of computers, its unlikely everything goes right the first time around. If you have any issues, don't be afraid to contact me on discord! I can usually be contacted in the EU4 Modder's Discord: https://discord.gg/F36vpqH, and I reside in the EST timezone (Eastern Standard Time, east coast America).

(Seriously, please don't be afraid to ask for help. It brings me joy to see other people enjoying my creations, be it my EU4 Mod(s) or Tools. I want to see you and your dream mod succeed.)
