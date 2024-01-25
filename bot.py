import discord
import os
from datetime import datetime
from realm_status import RealmStatus

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
# intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

realmStatus = RealmStatus()


@client.event
async def on_ready():
    print(f"Logged in as: {client.user}")
    print(f"Syncing command tree")
    await tree.sync()

    print(f"Starting webdriver")
    realmStatus.start()


@tree.command(
    name="wowstatus",
    description="Retrieve the current status of all EU realms"
)
async def on_wow_status(interaction):
    # Create/Edit version
    loading_embed_msg = discord.Embed(title="Season of Discovery Realm Status", description="Refreshing realm status <a:Loading:1199860788240859227>")
    status_msg = await interaction.response.send_message(embed=loading_embed_msg)

    embed_msg = discord.Embed(title="Season of Discovery Realm Status", description="The current status of all EU realms", timestamp=datetime.now())
    realms = realmStatus.retrieve_realms()
    
    for name, status in realms.items():
        embed_msg.add_field(name=name, value=RealmStatus.format_status(status))

    await interaction.edit_original_response(embed=embed_msg)


client.run(TOKEN)
