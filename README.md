# PMR446callsign

PMR446callsign is a telegram bot written in Python.

Needs pyhton..., pip, and sqlite3 to be installed on you system.

Tested...it works fine on a Docker Python container. I do see a reason it should not work on similar enviroments or other Python instances.

>> PLEASE NOTICE
Replace YOUR TELEGRAM TOKEN with your bot token, obtained from Telegram "BotFather". It's on lne 7. Also take a minute to change the password to a new one or else, everyone that knows this code will be able to delete your data. (/delete command is not working for now, but it will... It's on line 13)


Pleas take into account that
  The "generated_word.db" will be created when you run the script. This is where the call signs are being store.
  The script add a random number from 1 to 9999 to the word PMR. Reduce, enlarge of change the interval by modifing both lines 55 and 76



23 July 2023 -  version 0.1
- /delete command not working :(
- the bot misses a /start command to show a list of commands and description of bot.
- Not sure if the feature that check is the generated call sign exists on the database works.
