import random
import discord
from discord import app_commands
from discord.ext import commands


class wobux(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='wobux', description='sends a wobux image')
    async def wobux(self, interaction: discord.Interaction) -> None:
        wobuxs = [
            'https://tenor.com/view/wobux-gif-18616206',
            'https://tenor.com/view/brownis-tommy-mommy-gif-19092252',
            'https://tenor.com/view/robux-free-robux-meme-gif-23974928',
            'https://tenor.com/view/robux-roblox-roblox-noob-dancing-cash-money-gif-14858843',
            'https://tenor.com/view/give-me-robux-or-i-remove-mod-gif-23478510',
            'https://tenor.com/view/love-bobux-bobux-robux-roblox-heart-locket-gif-23421552',
            'https://tenor.com/view/roblox-robux-bobux-69bobux-gif-20072247',
            'https://tenor.com/view/wanna-play-wanna-play-roblox-roblox-cat-cat-jump-gif-24541774',
            'https://tenor.com/view/roblox-robux-gif-24770426',
            'https://tenor.com/view/bryce-popeyes-monkey-bryce-robux-robux-gif-21326781'
        ]

        # choose a random wobux
        wobux_img = wobuxs[random.randint(0, len(wobuxs))]

        await interaction.response.send_message(wobux_img)

