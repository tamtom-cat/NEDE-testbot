import discord
from discord import app_commands
import discord_func as func

class qoll(discord.ui.View):
    async def __init__(self, timeout=None):
        super().__init__(timeout=timeout)
        self.title = None
        self.message = None
        self.choices = None
        self.arg_limit = None
        self.arg_option = None
        self.arg_result = None        

class set_poll_Modal(discord.ui.Modal):
    def __init__(self, Modal_title, args, qoll_cls):
        super().__init__(title=Modal_title)
        self.qoll=qoll_cls
        
        for i in range(3):
            item=discord.ui.TextInput(
                label=args.labels[i],
                style=args.styles[i],
                required=args.requireds[i],
                placeholder=args.placeholders[i] 
            )
            self.add_item(item)
    
    async def on_submit(self, interaction: discord.Interaction):
        self.qoll.title = self.children[0].value
        self.qoll.message = self.children[1].value
        self.qoll.choices = self.children[2].value

        await interaction.response.send_message(
            content="こんな感じでOK?\nOKなら期限を設定してね！",
            embed=self.qoll.make_preview_embed(),
            view=self.qoll.add_button(),
            ephemeral=True)

class set_button(discord.ui.Button):
    def __init__(self, mes: str, txt: str, color: discord.ButtonStyle, view: discord.ui.Button):
        super().__init__(label=txt, style=color)
    
    async def callback(self, interaction:discord.Interaction):
        await interaction.response.edit_message(content="", embed=None, view=None)#時間(30sくらい)で消えるようにする
        await interaction.channel.send(content=None, embed=self.add_embed())#ここを投票メッセージに変える

    
    
