#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 16:21:50 2022

@author: unitom
"""
import discord
import wrap.discord_class as mycls
import wrap.discord_func as myfunc

class make_view(discord.ui.View):
    """
    Magic Method 
    ------------
    __call__(
        items: list[discord.ui.Button | discord.ui.Select] | None,
        is_clear: bool = False
    ) -> None:

        add or renew the view.

    Parameter
    ------------
    interaction: discord.Interaction
        Interaction to get the message that this view belongs to.
    items: list[discord.ui.Button | discord.ui.Select]
        .
    is_editable: bool
        Whether the option can be reselected.
        The default is False.
    timeout: float | None
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If None then there is no timeout.
    
    Attribute
    ------------
    view_msg: discord.InteractionMessage
        .
    is_edit: bool
        .
    num: int
        .
    last_interaction: discord.Interaction | None
        .
    last_item: discord.ui.Button | discord.ui.Select | None
        .
    is_end: bool
        .
    items: list[discord.ui.Button | discord.ui.Select]
        .
    

    """
    def __init__(
        self,
        interaction: discord.Interaction,
        items: list[discord.ui.Button | discord.ui.Select] | None,
        is_edit: bool = True,
        timeout: float | None = None
        ):

        super().__init__(timeout = timeout)
        self.is_editable = is_edit
        self.num = 0
        self.last_interaction: discord.Interaction | None = None
        self.last_item: discord.ui.Button | discord.ui.Select | None = None
        self.is_end: bool = False
        if items != None:
            for item in items:
                self.num += 1#個数確認とかにつかうかも
                self.add_item(item)

    #add or renew the view
    def __call__(self, items: list[discord.ui.Button | discord.ui.Select] | None, is_clear: bool = False):
        #Clear the item if is_clear is true
        if is_clear == True:
            self.clear_items()
        
        #add item
        if items != None:
            for item in items:
                self.num += 1#個数確認とかにつかうかも
                self.add_item(item)
    
    #dissabled the UI of this view
    async def _end_UI(self):
        self.is_end = True

        for child in self.children:
            child.disabled = True
        
        await self.last_interaction.response.edit_message(view = self)

    #When the view interaction call    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #set interaction info
        self.last_interaction = interaction

        #If is_editable is False, disabled all view
        if self.is_editable == True:
            pass
        else:
            await self._end_UI()

        return await super().interaction_check(interaction)  

class make_select(discord.ui.Select):
    """
    Parameter
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
    
    Attribute
    ------------
    op_num: int
        Number of options attached to this UI view.
    is_once: bool
        Whether the option can be reselected.
    data_dict: dict[discord.Member, list[str]] | None
        The dictionary of user and values that have been selected by the user.
    disabled: bool
        Whether this UI view is disabled or not.

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
        self.op_num: int = 0
        self.is_once: bool = is_once
        self.data_dict: dict[discord.Member, list[str]] | None = None
        self.disabled: bool = False

        self._set_SelectOption(choices)
    
    def _set_SelectOption(self, choices):
        for choice in choices:
            self.op_num += 1#個数制限とかにつかうかも
            super().add_option(**choice)

    def _make_data_dict(self, interaction: discord.Interaction):
        #renew data_dict or set dict
        if interaction.user in self.data_dict:
            self.data_dict[interaction.user] = self.values
        else:
            self.data_dict.setdefault(interaction.user, self.values)

    async def callback(self, interaction:discord.Interaction):
        #set data_dict
        self._make_data_dict(interaction)

        #judge the flag and set config
        if self.is_once == True:
            self.disabled = True

class make_button(discord.ui.Button):
    """
    Parameter
    ------------
    label: str
        .
    color: discord.ButtonStyle = discord.ButtonStyle.primary
        .
    is_once: bool = False
        .
    is_public: bool = True
        .

    kwarg Parameters
    ------------
    custom_id: Optional[str]
        The ID of the button that gets received during an interaction.
        If this button is for a URL, it does not have a custom ID.
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
    
    Attribute
    ------------
    default_color: discord.ButtonStyle
        ButtonStyle set as initial value.
    data_dict: dict[discord.Member, bool] | None
        A dictionary of users and whether the button was pressed by that user.
    is_once: bool
        Whether the button can be pressed again.
    is_public: bool
        Whether the button is public.
    disabled: bool
        Whether this UI view is disabled or not.
    style: discord.ButtonStyle
        Reflecting ButtonStyle.
    Button_interaction: discord.Interaction
        Interaction of this Button.
        When overriding the callback function,
        the response to this interaction must always be called immediately after this button is pressed by the user.
    label: str
        label of this button.
    """
    def __init__(
        self,
        label: str,
        color: discord.ButtonStyle = discord.ButtonStyle.primary,
        is_once: bool = False,
        is_public: bool = True,
        **kwarg
        ):
        
        super().__init__(label = label, style = color, **kwarg)
        self.label = label
        self.default_color: discord.ButtonStyle = color
        self.is_once: bool = is_once
        self.is_public: bool = is_public
        self.data_dict: dict[discord.Member, bool] = {}
    
    def _make_data_dict(self, interaction: discord.Interaction):
        #switch data_dict or set dict
        if interaction.user in self.data_dict:
            self.data_dict[interaction.user] = not self.data_dict[interaction.user]
        else:
            self.data_dict.setdefault(interaction.user, [True])

    async def callback(self, interaction: discord.Interaction):
        #switch data_dict or set dict
        self._make_data_dict(interaction)
     
        #judge the flag and set config
        if self.is_once == True:
            self.disabled = True
        elif self.is_public == True:
            pass
        elif self.data_dict[interaction.user] == True:
            self.style = self.default_color
        elif self.data_dict[interaction.user] == False:
            self.style = discord.ButtonStyle.secondary
        else:
            print("error")#なんかエラーを吐く
    
    #make confirm button
    @classmethod
    def confirm_buttons(cls):
        Yes = cls(label = "OK", color = discord.ButtonStyle.green, is_once = True)
        No = cls(label = "Cancel", color = discord.ButtonStyle.red, is_once = True)
        return [Yes, No]


class make_modal(discord.ui.Modal):
    """
    Parameter
    ------------
    Modal_title: str
        The title of the modal. Can only be up to 45 characters.
    Modal_items: list[discord.TextInput]

    kwarg Parameter
    ------------
    timeout: Optional[float]
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If None then there is no timeout.
    custom_id: str
        The ID of the modal that gets received during an interaction.
        If not given then one is generated for you. Can only be up to 100 characters.
    
    Attribute
    ------------
    item_num:
        Number of options attached to this UI view.
    data_dict:

    children:

    Modal_interaction: discord.Interaction
        Interaction of this modal.
        The response to this interaction must always be called immediately after data is sent through this modal.
    """
    def __init__(
        self,
        Modal_title: str,
        Modal_items: list[discord.TextInput],
        **kwarg
        ):

        super().__init__(title = Modal_title, **kwarg)
        self.item_num: int = 0
        self.data_dict: dict[discord.Member, list[discord.ui.TextInput]] = {}

        self._set_TextInput(Modal_items)
    
    def _set_TextInput(self, Modal_items):
        for item in Modal_items:
            self.item_num += 1#個数制限とかにつかうかも
            super().add_item(item)
    
    def _make_data_dict(self, interaction: discord.Interaction):
        data_list = []

        for child in self.children:
            data_list.append(child)
        self.data_dict.setdefault(interaction.user, data_list)

    async def on_submit(self, interaction: discord.Interaction):
        self._make_data_dict(interaction)
        self.interaction = interaction
    
    @classmethod
    async def select_maker(cls, interaction: discord.Interaction):
        #set Modal data
        item = discord.ui.TextInput(
            label =  "選択肢を１行ごとに入力してね！",
            style = discord.TextStyle.long,
            required = 0,
            placeholder = "選択肢1\n選択肢2\n..."
            )
        
        #send Modal
        Modal = cls("セレクトメイカー", item)
        await interaction.response.send_modal(Modal)
        await Modal.wait()

        #get select data
        data = Modal.data_dict[interaction.user]
        labels = data[0].value.split()

        #make discord.select list
        selects = []
        for label in labels:
            selects.append(make_button(label = label))
        
        #return select list and Modal interaction
        return selects, Modal.Modal_interaction
    
    @classmethod
    async def button_maker(cls, interaction: discord.Interaction):
        #set Modal data
        item = discord.ui.TextInput(
            label =  "ボタンのラベル(選択肢)を１行ごとに入力してね！",
            style = discord.TextStyle.long,
            required = 0,
            placeholder = "ラベル名1\nラベル名2\n..."
            )
        
        #send Modal
        Modal = cls("ボタンメイカー", item)
        await interaction.response.send_modal(Modal)
        await Modal.wait()

        #get button data
        data = Modal.data_dict[interaction.user]
        labels = data[0].value.split()

        #make discord.button list
        buttons = []
        for label in labels:
            buttons.append(make_button(label = label))
        
        #return button list and Modal interaction
        return buttons, Modal.Modal_interaction
    
    @classmethod#未編集
    async def Modal_maker(cls, interaction: discord.Interaction):
        #set Modal data
        item = discord.ui.TextInput(
            label =  "ボタンのラベル(選択肢)を１行ごとに入力してね！",
            style = discord.TextStyle.long,
            required = 0,
            placeholder = "ラベル名1\nラベル名2\n..."
            )
        
        #send Modal
        Modal = cls("ボタンメイカー", item)
        await interaction.response.send_modal(Modal)
        await Modal.wait()

        #get button data
        data = Modal.data_dict[interaction.user]
        labels = data[0].value.split()

        #make discord.button list
        buttons = []
        for label in labels:
            buttons.append(make_button(label = label))
        
        #return button list and Modal interaction
        return buttons, Modal.Modal_interaction



if __name__ == "__main__":
    print(discord.__version__)