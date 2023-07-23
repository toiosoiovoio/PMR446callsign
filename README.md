# PMR446callsign

PMR446callsign is a telegram bot writing in Python.

Needs pyhton..., pip, and sqlite3 to be installed on you system.

Tested...it works fine on a Docker Python container. I do see a reason it should not work on similar enviroments or other Python instances.

Replace YOUR TELEGRAM TOKEN with you bot token obtained from Telegram "BotFather"


Pleas take into account that
  The "generated_word.db" will be created when you run the script. This is where the call sign are being store.
  the call sign is generated a interval the goes from 1 to 9999. Reduce or enlarge it by modifing line 55 and 76



23 July 2023 -  version 0.1
- /delete command not working :(
- the bot misses a /start with list of commands and description.
- Not sure if the feature that check is the generated call sign exists on the database works.
