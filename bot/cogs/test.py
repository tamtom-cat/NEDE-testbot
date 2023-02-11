import discord
from discord import app_commands
from discord.ext import commands

import wrap.discord_class as mycls
import wrap.discord_func as myfunc
import text.env_text as env

class Test_view(discord.ui.View):
    def __init__(self, timeout: float | None = None):
        super().__init__(timeout=timeout)
        self.is_open: bool = False

class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name = "test", description = "Test cog")
    async def Test(self, interaction: discord.Interaction) -> None:
        """/unload"""
        await interaction.response.send_message("hoge")

async def setup(bot: commands.Bot):
    await bot.add_cog(test(bot),  guild = discord.Object(id = env.Guild_id))
    
    
