import discord
import os
import json
import re
from discord.ext import commands
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def load_concerning_keywords():
    keywords = set()
    try:
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/concerningwords.txt"))
        with open(database_path, "r", encoding="utf-8") as file:
            keywords = {line.strip().lower() for line in file if line.strip()}
        print(f"✅ Loaded {len(keywords)} concerning keywords.")
    except Exception as e:
        print(f"⚠️ Error loading concerning words: {e}")
    return keywords

def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()

class MessageLogger(commands.Cog, name="MessageLogger"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.message_cache = {}
        self.concerning_keywords = load_concerning_keywords()
        self.analyzer = SentimentIntensityAnalyzer()

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ MessageLogger is active and tracking messages!")
        self.concerning_keywords = load_concerning_keywords()
        await self.bot.change_presence(activity=discord.Game(name="Checking messages..."))
        await self.fetch_past_messages()
        await self.bot.change_presence(activity=discord.Game(name="Done"))

    async def fetch_past_messages(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit=None, oldest_first=True):
                        if not message.author.bot:
                            await self.check_concerning_keywords(message)
                    print(f"✅ Fetched past messages from #{channel.name} in {guild.name}")
                except discord.errors.Forbidden:
                    print(f"⚠️ No permission to read history in #{channel.name}")

    async def check_concerning_keywords(self, message):
        content = clean_text(message.content)
        words = set(content.split())

        if any(keyword in words for keyword in self.concerning_keywords):
            await self.log_concerning_message(message, "Keyword detected")

        sentiment_score = self.analyzer.polarity_scores(message.content)
        if sentiment_score['compound'] <= -0.7:
            await self.log_concerning_message(message, "Negative sentiment detected")

    async def log_concerning_message(self, message, reason):
        log_file_path = os.path.join(LOG_DIR, "concerning_messages_log.txt")
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write("⚠️ Concerning Message Detected ⚠️\n")
            log_file.write(f"👤 User: {message.author} (ID: {message.author.id})\n")
            log_file.write(f"📅 Time: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"📌 Channel: #{message.channel.name}\n")
            log_file.write(f"📍 Reason: {reason}\n")
            log_file.write("🔽 Context:\n")

            if message.channel.id in self.message_cache:
                context_messages = self.message_cache[message.channel.id]
                prev_msg = next((msg for msg in reversed(context_messages) if msg.id != message.id), None)
                next_msg = None

                async for msg in message.channel.history(limit=2, after=message):
                    next_msg = msg
                    break

                if prev_msg:
                    log_file.write(f"     💬 {prev_msg.author}: {prev_msg.content}\n")
                log_file.write(f"     💬 {message.author}: {message.content}\n")
                if next_msg:
                    log_file.write(f"     💬 {next_msg.author}: {next_msg.content}\n")
            else:
                log_file.write(f"     💬 {message.author}: {message.content}\n")
            
            log_file.write("—" * 80 + "\n\n")

        print(f"⚠️ Logged concerning message from {message.author} for reason: {reason}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        channel_id = message.channel.id
        if channel_id not in self.message_cache:
            self.message_cache[channel_id] = []
        self.message_cache[channel_id].append(message)
        if len(self.message_cache[channel_id]) > 5:
            self.message_cache[channel_id].pop(0)

        print(f"Checking message: '{message.content}'")
        await self.check_concerning_keywords(message)

async def setup(bot) -> None:
    await bot.add_cog(MessageLogger(bot))
