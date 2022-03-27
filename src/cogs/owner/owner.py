import discord
from discord import app_commands
from discord.ext import commands


class owner(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='eval', description='evaluate')
    async def eval(self, interaction: discord.Interaction, code: str) -> None:
        if await interaction.client.is_owner(interaction.user):
            try:
                result = eval(code)
                await interaction.response.send_message(f'> {result}', ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f'`{e}`', ephemeral=True)
        else:
            await interaction.response.send_message(f'You are not the owner of me.', ephemeral=True)

    @app_commands.command(name='load', description='load or reload a cog')
    async def load(self, interaction: discord.Interaction, cog: str, reload: bool) -> None:
        if await interaction.client.is_owner(interaction.user):
            try:
                if reload:
                    await interaction.response.send_message(f'Reloading `{cog}`...', ephemeral=True)
                    await self.bot.reload_extension(cog)
                    await interaction.edit_original_message(content=f'Reloaded `{cog}`!')
                else:
                    await interaction.response.send_message(f'Loading `{cog}`...', ephemeral=True)
                    await self.bot.load_extension(cog)
                    await interaction.edit_original_message(content=f'Loaded `{cog}`!')
            except Exception as e:
                await interaction.response.send_message(f'`{e}`', ephemeral=True)
        else:
            await interaction.response.send_message(f'You are not the owner of me.', ephemeral=True)

    @app_commands.command(name='check_perms', description='check the permissions of the user')
    async def check_perms(self, interaction: discord.Interaction, permissions: str, user: discord.User) -> None:
        from src.perms import perms

        # check if author is bot owner
        if await perms(interaction, 'bot_owner'):
            # run perms
            result = await perms(interaction, permissions, user)

            # send result
            await interaction.response.send_message(f'{result}', ephemeral=True)

        else:
            await interaction.response.send_message(f'You are not the owner of me.', ephemeral=True)
