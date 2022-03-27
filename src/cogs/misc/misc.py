import discord
from discord import app_commands
from discord.ext import commands


class misc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='ping', description='replies pong')
    async def ping(self, interaction: discord.Interaction) -> None:
        import asyncio

        await interaction.response.send_message('Pong')
        await asyncio.sleep(.5)
        await interaction.edit_original_message(content='Pong.')
        await asyncio.sleep(.5)
        await interaction.edit_original_message(content='Pong..')
        await asyncio.sleep(.5)
        await interaction.edit_original_message(content='Pong...')
        await asyncio.sleep(.5)
        await interaction.edit_original_message(content=f'Pong! `{self.bot.latency * 1000:.2f} ms`')

    @app_commands.command(name='say', description='makes the bot say something')
    async def say(self, interaction: discord.Interaction, message: str) -> None:
        import re

        message = re.sub('(<@.*>)', '`\\1`', message)
        message = message.replace('@everyone', '`@everyone`')
        message = message.replace('@here', '`@here`')

        await interaction.response.send_message(f'> {message}')

    @app_commands.command(name='avatar', description='shows the avatar of the user')
    async def avatar(self, interaction: discord.Interaction, user: discord.User, ephemeral: bool) -> None:
        await interaction.response.send_message(embed=discord.Embed(title=user.name + '\'s avatar').set_image(url=user.display_avatar), ephemeral=ephemeral)
