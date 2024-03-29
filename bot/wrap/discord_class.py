import wrap.discord_func as myfunc
from dataclasses import dataclass
import discord

@dataclass
class ui_Data:
    #textdataの属性を追加する
    """
    Attributes
    ------------
    title: str
        Title of this data.
        The defaut is None.
    label: str
        Display labels for users.
        The defaut is None.
    value: Optional[Union[str, int]]
        The value of this label.
        The defaut is None.
    """
    title: str | None = None
    label: str | None = None
    value: str | int | None = None



class make_embed(discord.Embed):
    """
    Parameters
    -----------
    interaction: discord.Interaction
        An interaction happens when a user does an action that needs to be notified.
        Current examples are slash commands and components.
    fields: Optional[list[TextData]]
        A "field" is an "embedded" element consisting of a set of "name" and "value",
        and fields is list of its data.
        The default is None.
        Specify this when you want to dynamically add a "field" (from input). 
        This argument can be specified by an instance of the "TextData" class.
        When "field" is added dynamically, the "inline" attribute is automatically set to True;
        if you wish to change the "inline" attribute, use the "add_field" method.
        If you want to add a field statically (by code), use the "add_field" method.

    kwarg Parameters
    -----------
    title: Optional[:class:`str`]
        The title of the embed.
        This can be set during initialisation.
        Can only be up to 256 characters.
    type: :class:`str`
        The type of embed. Usually "rich".
        This can be set during initialisation.
        Possible strings for embed types can be found on discord's
        :ddocs:`api docs <resources/channel#embed-object-embed-types>`
    description: Optional[:class:`str`]
        The description of the embed.
        This can be set during initialisation.
        Can only be up to 4096 characters.
    url: Optional[:class:`str`]
        The URL of the embed.
        This can be set during initialisation.
    timestamp: Optional[:class:`datetime.datetime`]
        The timestamp of the embed content. This is an aware datetime.
        If a naive datetime is passed, it is converted to an aware
        datetime with the local timezone. If None, it is set automatically.
    colour: Optional[Union[:class:`Colour`, :class:`int`]]
        The colour code of the embed. Aliased to ``color`` as well.
        This can be set during initialisation.
    """
    def __init__(
        self,
        interaction: discord.Interaction | None = None,
        fields: list[ui_Data] | None = None, #ここはTextdata　dataclassをとれるようにする
        **kwarg
        ):

        self._set_default(interaction)
        self._set_fields(fields)

        super().__init__(**kwarg)
    
    def _set_default(self, interaction):
        #Color, embedの作成時間(JST)を設定 
        self.colour = discord.Color.purple()
        self.timestamp = myfunc.get_JST_time()

        #インタラクションの発行者情報(name, icon, dmへのリンク)
        if interaction != None:
            super().set_author(
                name = interaction.user.display_name,
                url = interaction.user.dm_channel.jump_url if interaction.user.dm_channel is not None else None,
                icon_url = myfunc.get_avatar_url(interaction.user)
            )
    
    def _set_fields(self, fields):
        #fields変数が渡された時、
        if fields != None:
            for field in fields:
                #valueをもつならその値を設定、持たない時は空白文字を設定
                if field.value == None:
                    super().add_field(name = field.label, value = '\u0000')
                else:
                    super().add_field(name = field.label, value = field.value)