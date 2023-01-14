#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:13:55 2022

@author: unitom
"""
import discord
from discord import app_commands
import discord_func as myfunc
import discord_class as mycls
import UI_kit as UI
import text

class poll_info():
    def __init__(self):
        self.labels = text.Modal_label
        self.styles = text.Modal_style
        self.requireds = text.Modal_req
        self.placeholders = text.Modal_ph

class poll():
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.stop = False
        self._set_info()
        #ここから

        #ここまで仮実装
        

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

        #set_data
        self.data = self.Modal.data_dict[self.interaction.user]
        self.title = self.data[0].value
        self.description = self.data[1].value
        self.selects = self.data[2].value.split()
        self.selects = [mycls.TextData(select) for select in self.selects]

        #update the intetaction
        self.interaction = self.Modal.Modal_interaction

    async def confirm(self):
        self.confirm_embed = mycls.make_embed(self.interaction, title = self.title, description = self.description, fields = self.selects)
        self.confirm_view = UI.add_view(self.interaction, UI.make_button.confirm_buttons(), is_edit = False)

        await self.interaction.response.send_message(
            embed = self.confirm_embed,
            view = self.confirm_view,
            ephemeral = True
        )
        await myfunc.wait_callback(self.confirm_view)
        self.interaction, self.item = self.confirm_view()
        
        if self.item.label == "Cancel":
            await self.interaction.response.send_message("投票を中止しました", ephemeral = True)
        #OKの時の処理を追加する

    def set_poll(self):
        while(self.stop != True):
            pass

    def end_poll(self):
        pass



        

if __name__ == "__main__":
    print(discord.__version__)