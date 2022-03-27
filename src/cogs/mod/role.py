import discord
from discord import app_commands
from discord.ext import commands


class role(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='role', description='add or remove a role')
    async def role(self, interaction: discord.Interaction, user: discord.User, role: discord.Role) -> None:

        if await interaction.client.is_owner(interaction.user) or interaction.permissions.administrator:
            if role in user.roles:
                try:
                    await user.remove_roles(role)
                except discord.errors.Forbidden:
                    await interaction.response.send_message('I don\'t have permission to remove roles.', ephemeral=True)
                    return
                await interaction.response.send_message(f'Removed `{role.name}` from {user.name}.')
            else:
                try:
                    await user.add_roles(role)
                except discord.errors.Forbidden:
                    await interaction.response.send_message('I don\'t have permission to add roles.', ephemeral=True)
                    return
                await interaction.response.send_message(f'Added `{role.name}` to {user.name}.')
        else:
            await interaction.response.send_message('You are not the owner of me.', ephemeral=True)