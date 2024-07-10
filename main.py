import discord
import os
import json
import utils.completion as completion
from typing import Final
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

async def get_user_info(member: discord.Member):
    """Get information about a user."""
    user_info = {
        'name': member.name,
        'id': member.id,
        'status': str(member.status),
        'joined_at': member.joined_at.isoformat(),
        'avatar' : member.avatar.url,
        'nickname' : member.nick
    }
    return json.dumps(user_info)

async def search_users(guild, attribute, value):
    users = {}
    for member in guild.members:
        users[member.id] = {
            'name': member.name.lower(),
            'nickname' : member.nick,
            'id': member.id,
            'avatar' : member.avatar.url,
            'joined_at': member.joined_at.isoformat(),
            'role': [role.name.lower() for role in member.roles]
        }

    matching_users = []
    for user_id, data in users.items():
        if attribute in data:
            if attribute == 'role':
                if value.lower() in data[attribute]: 
                    matching_users.append(data)
            else:
                if data[attribute] == value.lower():  
                    matching_users.append(data)
    return 'Function returned nothing, answer the question normally.' if json.dumps(matching_users) == '[]' else json.dumps(matching_users)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignore itself
    if message.author == client.user:
        return
    
    if message.content == 'Faust, back on the bus' and message.author.name == 'totallynotshid':
        await client.close()
    
    if client.user in message.mentions:
        prompt = message.content

        response = completion.general_completion(prompt) if message.author.name != 'totallynotshid' else completion.dante_completion(prompt)

        if response.choices[0].message.tool_calls:
            function_name = response.choices[0].message.tool_calls[0].function.name
            function_args = response.choices[0].message.tool_calls[0].function.arguments
            function_args_dict = json.loads(function_args)
            attribute = function_args_dict['attribute']
            value = function_args_dict['value']
            guild = message.guild

            if function_name == 'search_users':
                user_info = await search_users(guild, attribute, value)
                print(f"Searching: {attribute}, {value}")
                print(f"{user_info}")
                second_completion = await completion.function_completion(prompt, function_name, user_info)
                await message.channel.send(second_completion.choices[0].message.content)
        else:
            await message.channel.send(response.choices[0].message.content)

client.run(TOKEN)
