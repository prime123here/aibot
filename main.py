import discord
import re
from discord.ext import commands
import random
import asyncio

# Define the intents your bot will use
intents = discord.Intents.default()
intents.message_content = True  # Allows reading message content

# Initialize the bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)


# buy_pattern = re.compile(r'(how to|where to)(buy|purchase|)Ultimate blockRegen plugin', re.IGNORECASE)
# Define a regular expression pattern to match phrases related to plugin wikis
buy_pattern = re.compile(r'(how (can|do) I |where (can|do) I (buy|purchase) )Ultimate( |-)?BlockRegen( plugin)?', re.IGNORECASE)


plugin_wiki_pattern = re.compile(r'(is there a|where can I find a) wiki (for|about) (.+) plugin', re.IGNORECASE)
ticket_pattern = re.compile(r'(how to (make|create|open) a|how (can|do) I (make|create|open) a|where can I|how (can|do)'
                            r' I) ticket', re.IGNORECASE)
greeting_pattern = re.compile(r'^(hi|hello|hey|how\'?s? (it|everything) go(ing)?|what\'?s? up|sup|yo)\s*\??$',
                              re.IGNORECASE)

buy_responses = [
    f'You can purchase the Ultimate Blockregen plugin by heading over to the <#{1126207483841618066}>.',
    f'You can buy the Ultimate Blockregen plugin by heading over to the <#{1126207483841618066}>.',
    f'You can purchase the Ultimate Blockregen plugin by going to the <#{1126207483841618066}>.',
    f'You can buy the Ultimate Blockregen plugin by going to the <#{1126207483841618066}>.'
]


greeting_responses = [
    "Hello!",
    "Hi there!",
    "Hey!",
    "Greetings!",
    "Hello! How can I assist you today?",
    "Hi! What can I do for you?",
]



# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


# Event handler for when a message is received
@bot.event
async def on_message(message):
    # Avoid an infinite loop by ignoring the bot's own messages
    if message.author == bot.user:
        return

    # Check if the message content matches the plugin wiki pattern
    match = plugin_wiki_pattern.search(message.content)
    if match:
        # Extract the plugin name from the matched message
        plugin_name = match.group(3)

        # Construct a response with the plugin name
        response = f'Yep! You can find information about the "{plugin_name}" plugin in its wiki. Here is the link: [https://roshan-x-hmmbo.gitbook.io/ultimate-blockregen/]'

        # Reply to the user
        await message.channel.send(response)
    match_2 = ticket_pattern.search(message.content)
    if match_2:
        print("yep working")
        # response_2 = f'You can make a ticket by heading over to this channel [#「🎫」support]'
        response_2 = f'You can make a ticket by heading over to <#{1043852443496239125}>.'
        await message.channel.send(response_2)
    match_3 = greeting_pattern.search(message.content)
    if match_3:
        # Select a random response from the list and send it
        response_3 = random.choice(greeting_responses)
        await message.channel.send(response_3)

    match_4 = buy_pattern.search(message.content)
    if match_4:
        print("working")
        # Respond to the user's intent to buy the plugin
        response_4 = random.choice(buy_responses)
        await message.channel.send(response_4)

@bot.command()
@commands.has_any_role('Prime', 'Owner')  # Only users with 'prime' or 'owner' role can use this command
# Only users with 'prime' or 'owner' role can use this command
async def delete(ctx, num_messages: int):
    if num_messages < 1:
        await ctx.send("Please provide a valid number of messages to delete.")
        return

    # Delete messages
    await ctx.channel.purge(limit=num_messages + 1)  # +1 to also remove the command message

# Command to mute a user
@bot.command()
@commands.has_any_role('Prime', 'Owner')  # Only users with 'prime' or 'owner' role can use this command
 # Only users with 'prime' or 'owner' role can use this command
async def mute(ctx, member: discord.Member):
    # Add a role to mute the user (you'll need to create a 'Muted' role in your server)
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if muted_role:
        await member.add_roles(muted_role)
        await ctx.send(f'{member.mention} has been muted.')

# Command to unmute a user
@bot.command()
@commands.has_any_role('Prime', 'Owner')  # Only users with 'prime' or 'owner' role can use this command
 # Only users with 'prime' or 'owner' role can use this command
async def unmute(ctx, member: discord.Member):
    # Remove the 'Muted' role to unmute the user
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if muted_role and muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted.')

# Command to ban a user
@bot.command()
@commands.has_any_role('Prime', 'Owner')  # Only users with 'prime' or 'owner' role can use this command
  # Only users with 'prime' or 'owner' role can use this command
async def ban(ctx, member: discord.Member):
    await ctx.guild.ban(member)
    await ctx.send(f'{member.mention} has been banned.')

# Command to unban a user
@bot.command()
@commands.has_any_role('Prime', 'Owner')  # Only users with 'prime' or 'owner' role can use this command
async def unban(ctx, user_id: int):
    # Fetch the banned users and search for the user ID
    banned_users = await ctx.guild.bans()
    for entry in banned_users:
        if entry.user.id == user_id:
            await ctx.guild.unban(entry.user)
            await ctx.send(f'User with ID {user_id} has been unbanned.')
            return

    await ctx.send(f'User with ID {user_id} is not banned.')



# Run the bot with your token
bot.run('Bottoken')
