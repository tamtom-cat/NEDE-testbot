import discord
from discord import app_commands
from discord.ext import commands

import os

import wrap.discord_class as mycls
import wrap.discord_func as myfunc
import text.env_text as env
import text.admin_text as admin_text

#dmに状態を通知する機能を追加する
class Cog_manager(commands.GroupCog, name = "cog"):
    and_list = []
    unfound_list = []
    unload_list = []

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.owner = discord.Object(id = env.bot_Owner_id) #複数人におくれるようにしたい
    
    async def load_cog(self) -> list:
        fail = []

        for cog in env.Cogs:
            try:
                await self.bot.load_extension(cog)
            except commands.ExtensionAlreadyLoaded:
                await self.bot.reload_extension(cog)    
            except Exception as e:
                #await myfunc.send_DM(self.owner, "**fail the loading Cog**", cog, e)
                print(e)
                fail.append(cog)
                self.unload_cog(cog)
        
        await self.bot.tree.sync(guild = discord.Object(id = env.Guild_id))

        return fail
    
    async def unload_cog(self, cog):
        is_fail = False

        try:
            await self.bot.unload_extension(cog)
        except commands.ExtensionNotLoaded:
            pass
        except Exception as e:
            await myfunc.send_DM(self.owner, "**fail the unloading Cog**", cog, e)
            is_fail = True    

        await self.bot.tree.sync(guild = discord.Object(id = env.Guild_id))
        
        return is_fail
    
    #Cogs変数と存在するCogファイルの比較
    @classmethod
    def Check_Cog(cls, interaction: discord.Interaction | None = None) -> discord.Embed:
        cog_files = []

        #cogディレクトリにある.pyファイルを取得
        path = "/Users/unitom/Desktop/Program/python/Discode/NEDE-testbot/bot/cogs"
        for file in os.listdir(path):
            base, ext = os.path.splitext(file)
            if ext == ".py":
                cog_files.append("cogs." + base)#"cogs.hoge"の形で取得

        cls.and_list = list(set(env.Cogs) & set(cog_files))
        cls.unload_list = list(set(cog_files) - set(env.Cogs))
        cls.unfound_list = list(set(env.Cogs) - set(cog_files))
        embed = admin_text.Cog_status_embed(interaction, cls.and_list, cls.unload_list, cls.unfound_list)
       
        return embed

    
    #load and reload all
    @app_commands.command(name = "load", description = "load and reload all cogs")
    async def load(self, interaction: discord.Interaction) -> None:
        """/load"""
        await interaction.response.defer(ephemeral = True)
        #Cogのロード
        fail = await self.load_cog()
        await interaction.followup.send("loaded!")
        
        #CogStatusの確認
        Status_embed = self.Check_Cog(interaction)

        #結果の通知
        await interaction.followup.send(content = "fail:{}".format(fail))
        await interaction.followup.send("Status", embed = Status_embed, ephemeral = True)

    #unload
    @app_commands.command(name = "unload", description = "unload cog")
    async def unload(self, interaction: discord.Interaction) -> None:
        """/unload"""
        #unloadするcogの選択(selectoption)
        del_Cogs = ""

        #Cogのアンロード
        is_fail = await self.unload_cog(del_Cogs)

        #結果の通知
        interaction.response.send_message(ephemeral = True)
    
    #check
    @app_commands.command(name = "check", description = "check cog")
    async def unload(self, interaction: discord.Interaction) -> None:
        """/check"""
        await interaction.response.defer(ephemeral = True)

        #CogStatusの確認
        Status_embed = self.Check_Cog(interaction)
        await interaction.followup.send("get embed!")

        #結果の通知
        print("send DM")
        await interaction.followup.send("hoge", embed = Status_embed, ephemeral = True)

#load_extension用
async def setup(bot: commands.Bot):
    await bot.add_cog(Cog_manager(bot), guild = discord.Object(id = env.Guild_id))
    