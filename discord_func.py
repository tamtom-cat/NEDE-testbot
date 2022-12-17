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

def get_avatar_url(member):
    if member.avatar==None:
        avatar_url='https://cdn.discordapp.com/embed/avatars/0.png'
        return avatar_url
    else:
        avatar_url = member.avatar.replace(format="png").url
        return avatar_url

class embed_option():
    def __init__(self, field_arg = None, author = None, footer = None):
        self.fields = self.make_fields(field_arg)
        self.author = self.set_author()
        self.footer = self.set_footer()
    
    def make_fields(self, field_arg):
        pass

def make_embed(
    title: str, description: str | None = None,
    color: discord.Color = discord.Color.purple(),
    embed_arg: embed_option | None = None
    ):

    embed=discord.Embed(
        title=title,
        color=color,
        description=description
    )

    if embed_arg != None:
        if embed_arg.author != None:
            embed.set_author(name=embed_arg.author.name, icon_url=embed_arg.author.avatar_url)

        if embed_arg.fields != None:
            for info in embed_arg.fields:
                embed.add_field(name=info.name, value=info.value, inline=info.inline)
        
        if embed_arg.footer != None:
            embed.set_footer(text="", icon_url="")
    

class Modal_info():
    def __init__(self):
        self.labels = text.Modal_label
        self.styles = text.Modal_style
        self.requireds = text.Modal_req
        self.placeholders = text.Modal_ph
        


    
        
        





if __name__ == "__main__":
    print(discord.__version__) 

