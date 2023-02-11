import wrap.discord_class as mycls
import wrap.discord_func as myfunc
"""
Cog status

🟢 loaded
```
・hoge
　　　latest synced in yyyy/mm/dd, hh:mm
```

🟡 not loaded
```
・fuga
　　　never loaded
・hogehoge
　　　unloaded in yyyy/mm/dd, hh:mm
```

🔴 unfound cog
```
・fugafuga
・hogeguga
```
"""


embed_title = "**Cog Status**"

loaded_title = "🟢 **loaded**\n"
loaded_mes = "latest synced in "

unloaded_title = "🟡 **not loaded**\n"
unloaded_never = "never loaded"
unloaded_past = "unloaded in "

unfound_title = "🔴 **unfound cog**\n"

def make_status_block(cogs: list, cog_type: str, cog_title: str) -> str:
    now = myfunc.get_JST_time()
    now = now.strftime("%Y/%m/%d, %H:%M:%S")
    Cog_status_mes = ""
    for cog in cogs:
        Cog_status_mes += "・{}\n".format(cog)
        if cog_type == "loaded":
            Cog_status_mes += ("\t" + loaded_mes + now + "\n")
        elif cog_type == "unloaded":
            pass
        elif cog_type == "unfound":
            print("unfound:\n", cog,)
    
    if Cog_status_mes == "":
        Cog_status_mes = "None!"        

    status_block = cog_title + "```" + Cog_status_mes + "```"
    return status_block

def Cog_status_embed(interaction, loaded_cog: list[str], unloaded_cog: list[str], unfound_cog: list[str]):
    Cog_text = ""
    cog_list = [loaded_cog, unloaded_cog, unfound_cog]
    cog_types = ["loaded", "unloaded", "unfound"]
    cog_titles = [loaded_title, unloaded_title, unfound_title]

    for cog_info in zip(cog_list, cog_types, cog_titles):
        Cog_text += make_status_block(*cog_info)
        Cog_text += "\n"

    Cog_embed = mycls.make_embed(interaction, title = embed_title, description = Cog_text)
    return Cog_embed

