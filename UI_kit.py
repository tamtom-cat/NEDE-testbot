#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 16:21:50 2022

@author: unitom
"""
import discord
from discord import app_commands
import discord_func as func

class poll(discord.ui.View):
    def __init__(self, bot_info, poll_author_info, title, message, choices, arg_limit, timeout=None):
        super().__init__(timeout=timeout)
        self.bot_info = bot_info
        self.author_info = poll_author_info
        self.title = title
        self.message = message
        self.choices = choices
        self.arg_limit = arg_limit

    def make_preview_embed(self):#期限も表示する
        preview_embed=discord.Embed(title=self.title,
                                 color=discord.Color.purple(),
                                 description=self.message
        )
        preview_embed.set_author(name=self.bot_info.display_name,
                              icon_url=self.bot_info.avatar_url
        )
        preview_embed.add_field(name=self.choices[0], value='\u0000', inline=True)
        preview_embed.add_field(name=self.choices[1], value='\u0000', inline=True)
        preview_embed.set_footer(text=f"made by {self.author_info.display_name}",
                              icon_url=self.author_info.avatar_url
        )

        return preview_embed
    
    @discord.ui.button(label="OK", style=discord.ButtonStyle.green)
    async def OK_button_callback(self, interaction:discord.Interaction, button:discord.ui.Button):#全然わからん！動くからヨシ！
        mes="投票を開始しました！"
        await interaction.response.edit_message(content=mes, embed=None, view=None)#時間(30sくらい)で消えるようにする
        await interaction.channel.send(content=None, embed=self.make_preview_embed())#ここを投票メッセージに変える

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def Cancel_button_callback(self, interaction:discord.Interaction, button:discord.ui.Button):
        mes="作成中の投票を削除しました"
        await interaction.response.edit_message(content=mes, embed=None, view=None)

#ここから下　新しい設計を描く
class make_view(discord.ui.View):
    def __init__(self, items: list[discord.ui.Button | discord.ui.Select], timeout: float | None = None):
        super().__init__(timeout = timeout)
        for item in items:
            self.num += 1#個数制限とかにつかうかも
            self.add_item(item)
    
    def make_items(self) -> list[discord.ui.Button | discord.ui.Select]:
        pass

class make_select(discord.ui.Select):
    def __init__(self, ):
        super().__init__()

class make_button(discord.ui.Button):
    def __init__(self, label: str, color: discord.ButtonStyle = discord.ButtonStyle.primary, is_once: bool = True):
        super().__init__(label = label, style = color)
        self.push_log: dict[discord.Member, bool] | None = None
        self.is_once: bool = is_once

    def get_push_data(self) -> dict[discord.Member, bool] | None:
        return self.push_log
    
    async def callback(self, interaction:discord.Interaction):
        #switch
        for dict in self.push_log:
            if interaction.user in dict:
                dict[interaction.user] = not dict[interaction.user]
            else:
                self.push_log.setdefault({interaction.user:True})
        
        if self.is_once == True:
            self.disabled = True
        elif self.push_log[interaction.user] == True:
            self.style = discord.ButtonStyle.primary
        elif self.push_log[interaction.user] == False:
            self.style = discord.ButtonStyle.secondary
        else:
            print("error")
        
        await interaction.response.edit_message(view=self)

class make_modal(discord.ui.Modal):
    def __init__(self, Modal_title, args):
        super().__init__(title=Modal_title)


"""    
class confirm_button(discord.ui.Button):
    def __init__(self, mes: str, txt: str, color: discord.ButtonStyle):
        super().__init__(label=txt, style=color)
        async def callback(self, interaction:discord.Interaction):
            await interaction.response.edit_message(content=mes, embed=None, view=None)#時間(30sくらい)で消えるようにする
            await interaction.channel.send(content=None, embed=self.make_preview_embed())#ここを投票メッセージに変える
        
    
    @discord.ui.button(label="OK", style=discord.ButtonStyle.green)
    

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def Cancel_button_callback(self, interaction:discord.Interaction, button:discord.ui.Button):
        mes="作成中の投票を削除しました"
        await interaction.response.edit_message(content=mes, embed=None, view=None)
"""

if __name__ == "__main__":
    print(discord.__version__)