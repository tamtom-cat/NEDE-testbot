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

@tree.command(name = "qoll", description = "テストコマンド", guild = discord.Object(id = Guild_id))
async def test(interaction: discord.Interaction, setting: bool=None):
    poll_author_info=interaction.user
    bot_info=interaction.guild.me #そもそも初めから引数として持て！
    qoll_view=tes.qoll(bot_info, poll_author_info, setting)
    Modal=tes.set_poll_Modal("投票を作成する", func.Modal_info(), qoll_view)
    await interaction.response.send_modal(Modal)

@tree.command(name = "poll", description = "投票コマンド", guild = discord.Object(id = Guild_id))
async def poll_maker(
    interaction: discord.Interaction,
    setting: bool = 0
):
    poll=poll()
"""
    await interaction.response.send_message(
        text.confirm_mes, embed=poll.make_preview_embed(),view=poll,
        ephemeral=True
    )
"""

boted.run(TOKEN)

if __name__=='__main__':
    print(discord.__version__)
    print(sys.version)
