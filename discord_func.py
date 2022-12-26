#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 22:56:16 2022

@author: unitom
"""
import discord
import text
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

def make_fields(name: list[str], value: list[str], inline: bool = True) -> list:
    pass

class Modal_info():
    def __init__(self):
        self.labels = text.Modal_label
        self.styles = text.Modal_style
        self.requireds = text.Modal_req
        self.placeholders = text.Modal_ph

if __name__ == "__main__":
    print(discord.__version__) 

