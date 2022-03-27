import discord
from discord import app_commands
from discord.ext import commands


class mod(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='purge', description='delete messages')
    async def purge(self, interaction: discord.Interaction, amount: int) -> None:
        if interaction.permissions.manage_messages or interaction.permissions.administrator:
            if amount > 100:
                amount = 100
            await interaction.response.send_message(f'Deleting `{amount}` messages...', ephemeral=True)
            try:
                await interaction.channel.purge(limit=amount, reason=f'Purged by {interaction.user.name}')
            except discord.errors.Forbidden:
                await interaction.edit_original_message(content=f'I don\'t have permission to delete messages.')
                return
            await interaction.edit_original_message(content=f'Deleted `{amount}` messages.')
        else:
            await interaction.response.send_message('You don\'t have permission to manage messages.', ephemeral=True)
