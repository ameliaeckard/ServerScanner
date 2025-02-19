import json
import logging
import os
import sys
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load configuration
if not os.path.isfile("config.json"):
    sys.exit("❌ 'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True

# Set up logging
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents)
        self.logger = logger
        self.config = config
        self.logged_users = set()

    async def setup_hook(self):
        """Runs when the bot starts to load cogs."""
        self.logger.info("🔄 Setting up the bot...")
        await self.load_cogs()

    async def load_cogs(self):
        """Loads all cogs from the 'cogs' directory."""
        cogs_directory = "cogs"
        if not os.path.exists(cogs_directory):
            self.logger.error(f"❌ Cogs directory '{cogs_directory}' not found!")
            return

        cog_files = [f[:-3] for f in os.listdir(cogs_directory) if f.endswith(".py")]

        if not cog_files:
            self.logger.warning("⚠️ No cog files found in the 'cogs' directory.")

        for cog in cog_files:
            cog_path = f"cogs.{cog}"
            try:
                self.logger.info(f"🔄 Loading cog: {cog_path}...")
                await self.load_extension(cog_path)
                self.logger.info(f"✅ Successfully loaded cog: {cog_path}")
            except Exception as e:
                self.logger.error(f"❌ Failed to load {cog_path}: {e}")

    async def on_message(self, message):
        """Handles incoming messages and logs user details."""
        if message.author.bot:
            return
        self.logged_users.add((message.author.id, message.author.name, message.author.created_at))
        await self.process_commands(message)

    async def fetch_past_users(self):
        """Fetches old user messages and logs them."""
        self.logger.info("🔄 Fetching past users from message history...")

        for guild in self.guilds:  # Loop through all servers the bot is in
            for channel in guild.text_channels:  # Loop through all text channels
                try:
                    async for message in channel.history(limit=1000):  # Adjust limit if needed
                        if not message.author.bot:
                            user_data = (message.author.id, message.author.name, message.author.created_at)
                            if user_data not in self.logged_users:
                                self.logged_users.add(user_data)
                    self.logger.info(f"✅ Fetched users from #{channel.name} in {guild.name}")
                except discord.errors.Forbidden:
                    self.logger.warning(f"⚠️ No permission to read history in #{channel.name}")

    async def on_ready(self):
        self.logger.info(f"✅ Logged in as {self.user.name}")
        await self.fetch_past_users()  # Fetch old messages


# Load environment variables and run the bot
load_dotenv()
bot = DiscordBot()
bot.run(os.getenv("TOKEN"))
