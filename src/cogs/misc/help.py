import discord
from discord import app_commands
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='help', description='shows this message')
    async def help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title='Help', description='This is a list of commands you can use.')

        embed.set_footer(text='https://github.com/m1ten/sentry-py')

        embed.set_author(name=self.bot.user.name)
        
        for cmd in self.bot.tree.get_commands(guild=interaction.guild):

            # check if command is owner only
            if cmd.owner_only:
                continue

            embed.add_field(name=cmd.name, value=cmd.description)

        await interaction.response.send_message(embed=embed)