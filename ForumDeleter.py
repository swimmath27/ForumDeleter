

import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'YOUR_BOT_TOKEN'
# Replace with your guild (server) ID
GUILD_ID = 123456789
# Replace with the ID of the forum channel you want to monitor
FORUM_CHANNEL_ID = 123456789
# Define the inactivity period (e.g., 7 days or 10 seconds).
# Remember to update how often the bot checks for inactive posts above the monitor_inactive_posts() method
INACTIVITY_PERIOD = timedelta(seconds=10)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    monitor_inactive_posts.start()

@tasks.loop(seconds=10)  # Check for inactive posts every 10 seconds
async def monitor_inactive_posts():
    guild = bot.get_guild(GUILD_ID)
    forum_channel = guild.get_channel(FORUM_CHANNEL_ID)
    
    if forum_channel is None:
        print(f"Forum channel with ID {FORUM_CHANNEL_ID} not found.")
        return

    now = datetime.now(timezone.utc)

    for thread in forum_channel.threads:
        # Get the last message in the thread
        last_message = await thread.fetch_message(thread.last_message_id)
        if last_message is None:
            continue

        last_message_time = last_message.created_at
        if (now - last_message_time) > INACTIVITY_PERIOD:
            await thread.delete()
            print(f"Deleted thread {thread.name} due to inactivity.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        raise error

# Run the bot
bot.run(TOKEN)
