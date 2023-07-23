import random
import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_API_TOKEN' with the actual token you obtained from BotFather
API_TOKEN = 'YOUR TELEGRAM TOKEN'

# SQLite database file
DB_FILE = 'generated_words.db'

# Password for deleting entries (replace with your desired password)
DELETE_PASSWORD = 'password'

# Function to create the SQLite database and table
def create_database():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT,
            first_name TEXT,
            last_name TEXT,
            nickname TEXT,
            location TEXT
        )
    ''')
    connection.commit()
    connection.close()

# Function to insert a record into the database
def insert_record(record):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO generated_records (word, first_name, last_name, nickname, location) VALUES (?, ?, ?, ?, ?)', record)
    connection.commit()
    connection.close()
        
# Function to check if the word exists in the database
def word_exists(word):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute('SELECT word FROM generated_records WHERE word = ?', (word,))
    result = cursor.fetchone()
    connection.close()
    return result is not None

# Command handler for the /generate command
def generate_word(update: Update, _: CallbackContext) -> None:
    context = _.user_data
    context["expected_field"] = "accept_word"

    while True:
        word = f"PMR{random.randint(1, 9999)}"
        if not word_exists(word):
            break
    context["generated_word"] = word

    # Ask the user if they accept the generated word
    update.message.reply_text(f"New call sign: {word}\nDo you accept this call sign? (yes/no)")

# Message handler to capture user response to accept the word or generate a replacement
def handle_accept_word(update: Update, _: CallbackContext) -> None:
    response = update.message.text.lower()
    context = _.user_data

    if "generated_word" in context and context.get("expected_field") == "accept_word":
        if response == "yes":
            # Proceed with asking for first name
            update.message.reply_text("Please enter your first name:")
            context["expected_field"] = "first_name"
        elif response == "no":
            # Generate a replacement word
            while True:
                word = f"PMR{random.randint(1, 9999)}"
                if not word_exists(word):
                    break
            context["generated_word"] = word
            update.message.reply_text(f"Alternative call sign: {word}\nDo you accept this call sign? (yes/no)")
        else:
            update.message.reply_text("Invalid response. Please reply with 'yes' or 'no'.")

    elif context.get("expected_field") == "first_name":
        first_name = update.message.text.strip()
        if not first_name:
            update.message.reply_text("First name cannot be blank. Please enter your first name:")
            return

        context["first_name"] = first_name
        update.message.reply_text("Please enter your last name:")
        context["expected_field"] = "last_name"

    elif context.get("expected_field") == "last_name":
        last_name = update.message.text.strip()
        if not last_name:
            update.message.reply_text("Last name cannot be blank. Please enter your last name:")
            return
        
        context["last_name"] = last_name
        update.message.reply_text("Please enter your nickname (or type 'skip' to skip this step):")
        context["expected_field"] = "nickname"

    elif context.get("expected_field") == "nickname":
        nickname = update.message.text.strip()
        if nickname.lower() == 'skip':
            nickname = None

        context["nickname"] = nickname
        update.message.reply_text("Please enter your location:")
        context["expected_field"] = "location"

    elif context.get("expected_field") == "location":
        location = update.message.text.strip()

        # All fields are collected, insert the record into the database
        generated_word = context["generated_word"]
        first_name = context["first_name"]
        last_name = context["last_name"]
        nickname = context["nickname"]
        insert_record((generated_word, first_name, last_name, nickname, location))

        # Clear the user data after processing
        context.clear()
        update.message.reply_text("Call sign has been saved successfully.")

    else:
        update.message.reply_text("Please generate a call sign first using the /generate command.")

def list_generated_records(update: Update, _: CallbackContext) -> None:
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM generated_records')
    records = cursor.fetchall()
    connection.close()

    if not records:
        update.message.reply_text("No records found.")
    else:
        result = "\n".join([f"Word: {record[1]}, First Name: {record[2]}, Last Name: {record[3]}, Nickname: {record[4] or '-'}, Location: {record[5]}" for record in records])
        update.message.reply_text(f"Generated records:\n{result}")
            
# Command handler for the /delete command
def delete_records(update: Update, _: CallbackContext) -> None:
    context = _.user_data
    context["expected_field"] = "confirm_delete"

    update.message.reply_text("Are you sure you want to delete all entries in the database? (yes/no)")

# Message handler to capture user response to confirm the delete operation and password
def handle_confirm_delete(update: Update, _: CallbackContext) -> None:
    response = update.message.text.lower()
    context = _.user_data

    if context.get("expected_field") == "confirm_delete":
        if response == "yes":
            update.message.reply_text("Please enter the password to confirm the delete operation:")

            # Update the expected field to password for verification
            context["expected_field"] = "password"
        elif response == "no":
            update.message.reply_text("Delete operation canceled.")
            context.clear()
        else:
            update.message.reply_text("Invalid response. Please reply with 'yes' or 'no'.")

    elif context.get("expected_field") == "password":
        password = update.message.text.strip()

        if password == DELETE_PASSWORD:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute('DELETE FROM generated_records')
            connection.commit()
            connection.close()

            update.message.reply_text("All entries in the database have been deleted.")
        else:
            update.message.reply_text("Incorrect password. Delete operation aborted.")

        # Clear the user data after processing
        context.clear()

def main() -> None:
    # Create the database and table if they don't exist
    create_database()

    # Create the Updater and pass it your bot's API token
    updater = Updater(API_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the message handler to capture user response to accept the word or generate a replacement
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_accept_word))

    # Register the /generate command handler
    dispatcher.add_handler(CommandHandler("generate", generate_word))

    # Register the /list command handler
    dispatcher.add_handler(CommandHandler("list", list_generated_records))
    
    # Register the /delete command handler
    dispatcher.add_handler(CommandHandler("delete", delete_records))

    # Register the message handler to capture user response to confirm the delete operation and password
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_confirm_delete))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()