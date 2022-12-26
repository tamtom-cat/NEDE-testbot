#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:13:55 2022

@author: unitom
"""
import discord
from discord import app_commands
import discord_func as func

class poll():
    def __init__(self, title: str = "投票", message: str | None = None, choices: str | None = None, arg_limit: None = None):
        self.title = title
        self.message = message
        self.choices = choices
        self.arg_limit = arg_limit

    def send_Modal():
        pass

if __name__ == "__main__":
    print(discord.__version__)