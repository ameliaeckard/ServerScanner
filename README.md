### **Discord Message Logger Bot**

## Overview
This bot monitors messages in a Discord server, **but only logs messages that are flagged** based on predefined keywords or sentiment analysis. **Users must be informed about the usage of the bot and its logging activities** before it is used.

## Features
- Logs usernames, user IDs, and account ages only when required for moderation purposes.
- Tracks and records messages only if they are flagged as concerning.
- Detects concerning messages based on a predefined keyword list and sentiment analysis.
- Flags concerning messages and logs them with context (previous and next messages).
- Stores flagged concerning messages in an organized log file for server moderation review.

## Usage
- **Important**: **This bot must be used only after informing users** that their messages will be monitored and logged in the event of concerning content being flagged.
- Simply add the bot to your Discord server, and it will start monitoring messages. If a message is flagged for concern, it will be logged with relevant details and context. **Only concerning messages will be logged.**
  
## Logs Format
```
⚠️ Concerning Message Detected ⚠️
👤 User: 
📅 Time:
📌 Channel:
📍 Reason:
🔽 Context:
     💬 user: message
————————————————————————————————————————
```

## Installation & Setup
1. Clone the repository.  
2. Open terminal.  
3. Navigate to the serverscanner directory using `cd serverscanner`.  
4. Go to `.env.txt` file and add the bot's TOKEN.
5. Rename `.env.txt` to `.env` 
6. Add the bot invite link to the config file.   
7. Install dependencies using `pip install -r requirements.txt`.
8. Run the bot by executing `python bot.py`.

## Notes
- The bot will only log **concerning messages**, **not all messages**.
- The concerning words list can be modified in `database/concerningwords.txt`.
- Make sure your server **informs all members** about the bot’s message monitoring and logging activities.