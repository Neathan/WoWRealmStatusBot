import discord
import os
from datetime import datetime
from realm_status import RealmStatus

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

realmStatus = RealmStatus()


@client.event
async def on_ready():
    print(f"Logged in as: {client.user}")
    realmStatus.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$status"):
        loading_embed_msg = discord.Embed(title="Season of Discovery Realm Status", description="Refreshing realm status <a:Loading:1199860788240859227>")
        status_msg = await message.channel.send(embed=loading_embed_msg)

        embed_msg = discord.Embed(title="Season of Discovery Realm Status", description="The current status of all EU realms", timestamp=datetime.now())
        realms = realmStatus.retrieve_realms()
        
        for name, status in realms.items():
            embed_msg.add_field(name=name, value=RealmStatus.format_status(status))

        await status_msg.delete()
        await message.channel.send(embed=embed_msg)

client.run(TOKEN)
