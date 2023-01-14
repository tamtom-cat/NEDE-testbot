#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 22:56:16 2022

@author: unitom
"""
import discord
import UI_kit as UI
import asyncio
from discord import app_commands
from datetime import datetime, timedelta, timezone


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

def add_interaction_log(view: UI.add_view, item: UI.make_button | UI.make_select, interaction: discord.Interaction) -> None:
    view.last_interaction = interaction
    view.last_item = item

async def wait_callback(view: UI.add_view):
    while(view.last_interaction == None):
        await asyncio.sleep(1)

def make_fields(name: list[str], value: list[str], inline: bool = True) -> list:
    pass

def set_TextData_from_Modal(interaction: discord.Interaction, Modal: UI.make_modal):
    pass


if __name__ == "__main__":
    print(discord.__version__) 

