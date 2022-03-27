import discord
from os import listdir
from os.path import isdir, isfile, join


async def setup(bot: discord.ext.commands.Bot) -> None:

    # load GUILD_ID from .env
    try:
        import dotenv
        import os

        dotenv.load_dotenv()

        GUILD_ID = os.getenv('GUILD_ID')
    except Exception as e:
        print(f'Error: {e}')
        exit(1)

    # get all folder in the cogs folder
    for folder in [f for f in listdir('src/cogs') if isdir(join('src/cogs', f))]:
        if folder == '__pycache__':
            continue

        # get all files in the folder
        for file in [f for f in listdir(f'src/cogs/{folder}') if isfile(join(f'src/cogs/{folder}', f))]:
            if file == '__init__.py':
                continue

            # get the file name without the extension
            name = file.split('.')[0]

            # import the class with the name 'name' from the file 'name.py'
            cog = getattr(__import__(
                f'src.cogs.{folder}.{name}', fromlist=[name]), name)

            # load the cog
            try:
                await bot.add_cog(cog(bot), guild=discord.Object(id=GUILD_ID))
            except Exception as e:
                print(f'Failed to load extension {folder}.{name}: {e}')
