#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 22:56:16 2022

@author: unitom
"""
import discord
from discord.ext import commands
from discord import app_commands

import wrap.UI_kit as UI

from datetime import datetime, timedelta, timezone
import asyncio

def get_JST_time():
    jst = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(jst)

def get_avatar_url(member) -> str:
    if member.avatar==None:
        avatar_url='https://cdn.discordapp.com/embed/avatars/0.png'
        return avatar_url
    else:
        avatar_url = member.avatar.replace(format="png").url
        return avatar_url

async def make_data_dict(self: discord.ui.View, interaction: discord.Interaction):
    label = interaction.extras
    user = interaction.user

async def loop(self, stop_time, view_msg):#仮実装 設計からやり直す
    while(self.is_end == False):
        await asyncio.sleep(1)

        creat_time = view_msg.created_at.astimezone(timezone(timedelta(hours=+9), 'JST'))
        timeout = time_check(stop_time)

        if timeout == True:
            self.is_end = True
        
        if self.is_end == True:
            break


async def time_check(stop_time):
    now = get_JST_time()
    delta = stop_time - now
    if delta.days < 0:
        return True
    else:
        return False

async def send_DM(bot: commands.Bot, user_id: int, embed: discord.Embed | None = None, *message: str):
    user = await bot.fetch_user(user_id)
    DM_Channel = await bot.create_dm(user)
    mes = "\n".join(message)
    if embed == None:
        await DM_Channel.send(content = mes)
    else:
        await DM_Channel.send(content = mes, embed = embed)



if __name__ == "__main__":
    print(discord.__version__) 

