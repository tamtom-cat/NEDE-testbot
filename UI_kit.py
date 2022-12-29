#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 16:21:50 2022

@author: unitom
"""
import discord
from discord import app_commands
import asyncio
import discord_func as func
import discord_class as cls

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

#ここから下　新しい設計を描く
class add_view(discord.ui.View):
    def __init__(
        self,
        items: list[discord.ui.Button | discord.ui.Select],
        timeout: float | None = None
        ):

        super().__init__(timeout = timeout)
        for item in items:
            self.num += 1#個数制限とかにつかうかも
            self.add_item(item)
    
    async def end_UI(self, interaction: discord.Interaction, is_edit = None) -> discord.InteractionMessage  | None:
        if is_edit == True:
            return interaction.original_response()
        else:
            interaction.original_response().reply(content = "Disabled this UI message")
            await asyncio.sleep(10)
            self.stop()
            return None

class make_select(discord.ui.Select):
    """
    parameter
    ------------
    choices: list[discord.SelectOption]
        Represents a select menu's option. 

    max: int

    min: int

    is_onece: bool
        Whether the option can be reselected.
        The default is False.

    kwarg Parameters
    ------------
    custom_id: :class:`str`
        The ID of the select menu that gets received during an interaction.
        If not given then one is generated for you.
    placeholder: Optional[str]
        The placeholder text that is shown if nothing is selected, if any.
    row: Optional[:class:`int`]
        The relative row this select menu belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """
    def __init__(
        self,
        choices: list[discord.SelectOption],
        max: int = 1,
        min: int = 1,
        is_once: bool = False,
        **kwarg
        ):

        super().__init__(self, max_values = max, min_values = min, **kwarg)
        self._set_SelectOption(choices)
        self.is_once: bool = is_once
        self.data_dict: dict[discord.Member, list[str]] | None = None
    
    def _set_SelectOption(self, choices):
        for choice in choices:
             super().add_option(**choice)
             self.op_num += 1#個数制限とかにつかうかも

    def _make_data_dict(self, interaction: discord.Interaction):
        if interaction.user in self.data_dict:
            self.data_dict[interaction.user] = self.values
        else:
            self.data_dict.setdefault(interaction, self.values)
    
    def get_select_data(self) -> dict[discord.Member, list[str]] | None:
        return self.data_dict

    async def callback(self, interaction:discord.Interaction):
        self._make_data_dict(interaction)

        if self.is_once == True:
            self.disabled = True
        
        await interaction.response.edit_message(view=self)


class make_button(discord.ui.Button):
    """
    kwarg Parameters
    ------------
    custom_id: Optional[str]
        The ID of the button that gets received during an interaction. If this button is for a URL, it does not have a custom ID.
    url: Optional[str]
        The URL this button sends you to.
    emoji: Optional[Union[.PartialEmoji, .Emoji, str]]
        The emoji of the button, if available.
    row: Optional[:class:`int`]
        The relative row this select menu belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """
    def __init__(
        self,
        label: str,
        color: discord.ButtonStyle = discord.ButtonStyle.primary,
        is_once: bool = False,
        **kwarg
        ):
        
        super().__init__(label = label, style = color, **kwarg)
        self.default_color = color
        self.push_log: dict[discord.Member, bool] | None = None
        self.is_once: bool = is_once

    def get_push_data(self) -> dict[discord.Member, bool] | None:
        return self.push_log
    
    async def callback(self, interaction: discord.Interaction):
        #switch or add to dict
        if interaction.user in self.push_log:
            self.push_log[interaction.user] = not self.push_log[interaction.user]
        else:
            self.push_log.setdefault(interaction.user, True)
        
        if self.is_once == True:
            self.disabled = True
        elif self.push_log[interaction.user] == True:
            self.style = self.default_color
        elif self.push_log[interaction.user] == False:
            self.style = discord.ButtonStyle.secondary
        else:
            print("error")#なんかエラーを吐く
        
        await interaction.response.edit_message(view=self)

class make_modal(discord.ui.Modal):
    def __init__(
        self,
        Modal_title: str,
        Modal_items: list[discord.TextInput],
        **kwarg
        ):

        super().__init__(title = Modal_title, **kwarg)
        self._set_TextInput(Modal_items)
        self.data_dict: dict[discord.Member, list[cls.TextData]] | None = None
    
    def _set_TextInput(self, Modal_items):
        for item in Modal_items:
             super().add_option(item)
             self.item_num += 1#個数制限とかにつかうかも
    
    def _make_data_dict(self, interaction: discord.Interaction):
        data_list = []
        for child in self.children:
            data_list.append(cls.TextData(child.label, child.value))     
        self.data_dict.setdefault(interaction.user, data_list)
    
    def get_modal_data(self) -> dict[discord.Member, list[cls.TextData]]:
        return self.data_dict

    async def on_submit(self, interaction: discord.Interaction):
        self._make_data_dict(interaction)


if __name__ == "__main__":
    print(discord.__version__)