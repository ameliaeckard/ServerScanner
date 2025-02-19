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
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the bot and let it log messages in your server.

## Notes
- The bot will only log messages from users and ignore bot messages.
- The concerning words list can be modified in `database/concerningwords.txt`.

Happy monitoring! 🚀

