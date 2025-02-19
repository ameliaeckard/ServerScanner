import discord
from discord.ext import commands
from datetime import datetime, timezone
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

class userInfo(commands.Cog, name="userinfo"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def fetch_all_users(self):
        """Fetches all users from all guilds by going through message history."""
        all_users = set()

        # Loop through all guilds the bot is in
        for guild in self.bot.guilds:
            # Loop through all text channels in the guild
            for channel in guild.text_channels:
                try:
                    # Fetch past messages (set a high limit, e.g., 1000 messages per channel)
                    async for message in channel.history(limit=1000):  
                        if message.author not in all_users:
                            all_users.add(message.author)

                except discord.errors.Forbidden:
                    # If the bot doesn't have permission to read the message history, ignore it
                    print(f"⚠️ No permission to read history in {channel.name}.")

        return all_users

    @commands.Cog.listener()
    async def on_ready(self):
        """This function runs when the bot starts and updates the log with usernames, user IDs, and account ages."""
        print("🔄 Updating user info...")

        all_users = await self.fetch_all_users()

        with open(os.path.join(LOG_DIR, "user_info_log.txt"), "a", encoding="utf-8") as log_file:
            for user in all_users:
                user_id = user.id
                username = user.name
                account_creation_time = user.created_at.replace(tzinfo=timezone.utc)
                account_age_days = (datetime.now(timezone.utc) - account_creation_time).days  # Age in days

                log_file.write(f"User ID: {user_id}, Username: {username}, Account Age (days): {account_age_days}\n")

        print("✅ User info updated successfully!")

async def setup(bot) -> None:
    await bot.add_cog(userInfo(bot))
