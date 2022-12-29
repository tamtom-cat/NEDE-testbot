#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:13:55 2022

@author: unitom
"""
import discord
from discord import app_commands
import discord_func as func
import UI_kit as UI
import discord_class as cls

class poll():
    def __init__(self, interaction: discord.Interaction):
        #ここから
        self.items = []
        self._temp(self.items)
        #ここまで仮実装
        self.Modal = UI.make_modal(title = "投票を作成する", Modal_items = self.items)
        interaction.response.send_modal(self.Modal)
        self._confirm(interaction)

    #仮実装用のメソッド
    async def _temp(self, item):
        args = func.Modal_info()
        for i in range(3):
            item=discord.ui.TextInput(
                label=args.labels[i],
                style=args.styles[i],
                required=args.requireds[i],
                placeholder=args.placeholders[i] 
            )
            self.items.append(item)
    
    def _confirm(self, interaction):
        #self.Modal.get_modal_data から情報をとって整理するプログラムを書く
        #title, description, selectsのvalueをforループで取得する。
        #selectについては改行ごとに分けて取得する
        self.title = self.Modal.get_modal_data[interaction.member][0].value
        self.description = self.Modal.get_modal_data[interaction.member][1].value
        self.selects = self.Modal.get_modal_data[interaction.member][2].value.split()
        cls.make_embed(interaction, title = self.title, description = self.description, fields = self.selects)
        

if __name__ == "__main__":
    print(discord.__version__)