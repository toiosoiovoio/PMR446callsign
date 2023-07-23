# PMR446callsign

PMR446callsign is a telegram bot written in Python.

Needs pyhton..., pip, and sqlite3 to be installed on you system.

Tested...it works fine on a Docker Python container. I do see a reason it should not work on similar enviroments or other Python instances.

>> PLEASE NOTICE
Replace YOUR TELEGRAM TOKEN with your bot token, obtained from Telegram "BotFather". It's on lne 7. Also take a minute to change the password to a new one or else, everyone that knows this code will be able to delete your data. (/delete command is not working for now, but it will... It's on line 13). Do not assune that this authentication method is a solid, bullet proof, fool proof, no risk and unhackable method. In fact it is not. So... NO WARRANTIES. IF YOUR DATA IS IMPORTANT TO YO, BACK IT UP!!!


Take into account that the "generated_word.db" will be created when you run the script. This is where the call signs are being store. The script adds a random number from 1 to 9999 to the word PMR. Reduce, enlarge of change the interval by modifing both lines 55 and 76. This file can be deleted to remove all call signs.



23 July 2023 -  version 0.1
- /delete all call signs command not working :(
- a selective /delete call sign will be a future feature.
- the bot misses a /start command to show a list of commands and description of bot.
- Not sure if the feature that check is the generated call sign exists on the database works... I'm a newbie!
