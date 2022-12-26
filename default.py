#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 20:15:48 2022

@author: unitom
"""
import sys

import time
import discord
from discord import app_commands

from UI_kit import poll
import test_class as tes
import discord_func as func
import text
#import env_text as env

TOKEN = env.TOKEN # TOKENを貼り付け
Guild_id = env.Guild_id #Guild_id を貼り付け

class bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
          
        
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = Guild_id))
            self.synced = True
        print('ログインしました')

boted = bot()
tree = app_commands.CommandTree(boted)

@tree.command(name = "command-name", description = "description", guild = discord.Object(id = Guild_id))
async def self(interaction: discord.Interaction, title: str):
    await interaction.response.send_message("")

@tree.command(name = "t", description = "description", guild = discord.Object(id = Guild_id))
async def self(interaction: discord.Interaction, title: str):
    await interaction.response.send_message(embed=func.make_embed(interaction, title = title))

@tree.command(name = "qoll", description = "テストコマンド1", guild = discord.Object(id = Guild_id))
async def test(interaction: discord.Interaction, setting: bool=None):
    poll_author_info=interaction.user
    bot_info=interaction.guild.me #そもそも初めから引数として持て！
    qoll_view=tes.qoll(bot_info, poll_author_info, setting)
    Modal=tes.set_poll_Modal("投票を作成する", func.Modal_info(), qoll_view)
    await interaction.response.send_modal(Modal)

@tree.command(name = "poll", description = "投票コマンド", guild = discord.Object(id = Guild_id))
async def poll_maker(
    interaction: discord.Interaction, title: str, message: str,
    limit_d: int=None, limit_h: int=None,limit_m: int=None, limit_s: int=None, limit_stop: int=None,
    choice1: str=None, choice2: str=None, choice3: str=None, choice4: str=None, choice5: str=None,
    choice6: str=None, choice7: str=None, choice8: str=None, choice9: str=None, choice10: str=None
):
    """投票を行うコマンド

    Parameters
        -----------
        title: str
            投票タイトル(質問内容)を入力してね！
        message: str
            細かい説明(詳細や補足など)を入力してね!
        choice: str
            選択肢を入力してね！
        setting: bool
            詳細設定をする場合は1を入力してね！
    """
    arg_limit=[limit_d, limit_h, limit_m, limit_s, limit_stop]
    choices=[choice1, choice2, choice3, choice4, choice5,choice6, choice7, choice8, choice9, choice10]
    poll=poll(title, message, choices, arg_limit)

    await interaction.response.send_message(
        text.confirm_mes, embed=poll.make_preview_embed(),view=poll,
        ephemeral=True
    )

boted.run(TOKEN)

if __name__=='__main__':
    print(discord.__version__)
    print(sys.version)
