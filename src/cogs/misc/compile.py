import discord
from discord import app_commands
from discord.ext import commands


class compile(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='compile', description='Compiles a code snippet')
    async def compile(self, interaction: discord.Interaction, lang: str, compiler: str, code: str, ephemeral: bool):
        import requests

        if not compiler or compiler == 'None':
            match lang:
                case 'c':
                    compiler = 'cg94'
                case 'python' | 'py':
                    compiler = 'python310'
                case 'ruby' | 'rb':
                    compiler = 'ruby302'
                case 'rust' | 'rs':
                    compiler = 'r190'
                case 'java' | 'jdk':
                    compiler = 'java1700'
                case _:
                    await interaction.response.message_send(f'Language {lang} is not supported')
            
            complier = str(compiler)

        # check if code is pastebin or github
        if ('https://pastebin.com/raw/' or 'https://gist.githubusercontent.com/' or 'https://www.toptal.com/developers/hastebin/raw/') in code:
            r = requests.get(code)
            code = r.text

        json_data = {
            "source": f"{code}",
            "compiler": f"{compiler}",
            "options": {
                "compilerOptions": {
                    "executorRequest": True
                },
                "filters": {
                    "execute": True
                },
            },
            "allowStoreCodeDebug": True
        }

        # compile the code
        response = requests.post(
            f'https://godbolt.org/api/compiler/{compiler}/compile', json=json_data)

        if 'Error 404' in response.text:
            await interaction.response.send_message(f'`{compiler}` is not a valid compiler.\nSee <https://godbolt.org/api/compilers/>.', ephemeral=True)
            return
        elif '# Compilation provided by Compiler Explorer at https://godbolt.org/' in response.text:
            text = response.text.replace(
                '# Compilation provided by Compiler Explorer at https://godbolt.org/', '')
        else:
            text = response.text

        lang = lang.capitalize()

        embed = discord.Embed(
            title=f'{lang}', color=0x000000, url=f'https://godbolt.org/')
        embed.add_field(
            name='Input', value=f'```{lang}\n{code[:1000]}```', inline=False)
        embed.add_field(
            name='Output', value=f'```{text[:1000]}```', inline=False)
        embed.set_footer(text=f'Powered by Godbolt - {compiler}')

        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
