import discord_func as func
from dataclasses import dataclass
import discord

class make_embed(discord.Embed):
    """
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
        interaction: discord.Interaction,
        fields: list[str, str, bool] | None = None,
        **kwarg
        ):

        self._set_default(interaction)
        self._set_fields()

        super().__init__(**kwarg)
    
    def _set_default(self, interaction):
        self.colour = discord.Color.purple()
        self.timestamp = interaction.created_at if interaction is not None else None
        super().set_author(
            name = interaction.user.display_name if interaction is not None else None,
            url = interaction.user.dm_channel.jump_url if interaction.user.dm_channel is not None else None,
            icon_url = func.get_avatar_url(interaction.user) if interaction is not None else None
        )
    
    def _set_fields(self, fields = None):

        if fields != None:
            for field in fields:
                super().add_field(name=field.name, value=field.value, inline=field.inline)


@dataclass
class TextData:
    """
    Attributes
    ------------
    label: str
        Display labels for users.
    value: Optional[Union[str, int]]
        The value of this label.
    """
    label: str
    value: str | int | None