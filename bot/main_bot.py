#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 20:15:48 2022

@author: unitom
"""
import sys

import discord
from discord.ext import commands

import wrap.discord_class as mycls
import wrap.discord_func as myfunc
import text.env_text as env
from cogs.Cog_manager import Cog_manager


TOKEN = env.TOKEN # TOKENを貼り付け
Guild_id = env.Guild_id #Guild_id を貼り付け
Cogs = env.Cogs

#Mybotを定義
class Mybot(commands.Bot):
    #cogの読み込みとコマンドのsyncを行う
    async def setup_hook(self: commands.Bot) -> None:
        for cog in Cogs:
            try:
                await self.load_extension(cog)
            except Exception as e:
                print(e)

    #Cogのリロード(更新)を行う
    async def on_ready(self: commands.Bot):
        #実行コンソールへの出力
        print('Logged in as')
        for cog in Cogs:
            try:
                await self.reload_extension(cog)
            except Exception as e:
                print(e)

        #リロードしたコグを再同期する
        await self.tree.sync(guild = discord.Object(id = env.Guild_id))
        print(self.user.name) #リロードの完遂を知らせる
        print('------')

        #discordでのCogStatusの出力
        await myfunc.send_DM(self, env.bot_Owner_id, Cog_manager.Check_Cog() ,"boot!")


#Mybotのインスタンスを作成
bot = Mybot(
    command_prefix="/",
    help_command=None,
    intents=discord.Intents.default()
    )

#Mybotを実行
bot.run(TOKEN)

if __name__=='__main__':
    print(discord.__version__)
    print(sys.version)
