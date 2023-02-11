# /poll UI-text
import discord

confirm_mes="下記のように投票を始めるよ！間違いがなければOK、間違いがあればCancelを押してね！"

Modal_label=["投票タイトル(質問内容)を入力してね！", "細かい説明(詳細や補足など)を入力してね!", "選択肢を１行ごとに入力してね！"]
Modal_style=[discord.TextStyle.short, discord.TextStyle.long, discord.TextStyle.long]
Modal_req=[0, 0, 0]
Modal_ph=["質問", "説明", "選択肢1\n選択肢2\n..."]

"投票を開始しました！"
# /name 

if __name__=='__main__':
    print("This is ",__file__)