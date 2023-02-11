#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:13:55 2022

@author: unitom
"""
import discord
from discord import app_commands
import bot.wrap.discord_func as myfunc
import bot.wrap.discord_class as mycls
import bot.wrap.UI_kit as UI
import bot.text.poll_text as poll_text

class poll_info():
    def __init__(self):
        self.labels = poll_text.Modal_label
        self.styles = poll_text.Modal_style
        self.requireds = poll_text.Modal_req
        self.placeholders = poll_text.Modal_ph

class poll():
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.poll_data = {}
        self.stop = False
        self._set_info()        

    def _set_info(self):
        self.items = []
        args = poll_info()
        for i in range(3):
            item=discord.ui.TextInput(
                label=args.labels[i],
                style=args.styles[i],
                required=args.requireds[i],
                placeholder=args.placeholders[i] 
            )
            self.items.append(item)
    
    async def set_data(self):#ここは外に出したほうがいいかも
        #send Modal
        self.Modal = UI.make_modal(Modal_title = "投票を作成する", Modal_items = self.items)
        await self.interaction.response.send_modal(self.Modal)
        await self.Modal.wait()

        #set_data ここはModalの機能に追加する
        self.data = self.Modal.data_dict[self.interaction.user]
        self.title = self.data[0].value
        self.description = self.data[1].value
        self.selects = self.data[2].value.split()
        self.selects = [mycls.ui_Data(select) for select in self.selects] #ui_data以外を使うように修正する

        #update the intetaction
        self.interaction = self.Modal.interaction

    async def confirm(self):
        self.confirm_embed = mycls.make_embed(self.interaction, title = self.title, description = self.description, fields = self.selects)
        self.confirm_view = UI.make_view(self.interaction, UI.make_button.confirm_buttons(), is_edit = False)

        await self.interaction.response.send_message(
            embed = self.confirm_embed,
            view = self.confirm_view,
            ephemeral = True
        )
        
        #ここで入力を検知(labelを確認)
          

def setup(bot):
    return bot.add_cog(poll(bot))

if __name__ == "__main__":
    print(discord.__version__)