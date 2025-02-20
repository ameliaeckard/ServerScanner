# Discord Message Logger Bot

## Overview
This bot logs user activity and chat messages in a Discord server. It also detects and flags concerning messages based on keyword detection and sentiment analysis.

## Features
- Logs usernames, user IDs, and account ages.
- Tracks and records chat messages.
- Detects concerning messages based on a predefined keyword list and sentiment analysis.
- Flags concerning messages and logs them with context (previous and next messages).
- Stores all concerning messages in an organized log file for review.

## Usage
Simply add the bot to your Discord server, and it will start monitoring messages. If a message is flagged, it will be logged with relevant details and context.

## Logs Format
```
⚠️ Concerning Message Detected ⚠️
👤 User: 
📅 Time:
📌 Channel:
📍 Reason:
🔽 Context:
     💬 user: previous message
————————————————————————————————————————
```

## Installation & Setup
1. Clone the repository.  
2. Open terminal.  
3. Navigate to the serverscanner directory using cd serverscanner.  
4. Go to .env.txt file and add the bot's TOKEN.
5. Rename .env.txt to .env 
6. Add the bot invite link to the config file.   
7. Install dependencies using pip install -r requirements.txt.
8. Run the bot by executing python bot.py.

## Notes
- The bot will only log messages from users and ignore bot messages.
- The concerning words list can be modified in `database/concerningwords.txt`.

Happy monitoring! 🚀