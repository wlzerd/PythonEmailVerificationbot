import datetime
import discord
import smtplib
import asyncio
import random
import time
from email.mime.text import MIMEText

client = discord.Client()

token = "ODExNDg5MTEzNTY3Nzg5MDU2.YCy8IQ.y3KEZHB-l-wxAb_wFxHa3sVqWsc"

@client.event
async def on_ready():
    print("시작")
    print(client.user)
    print("-------------")

@client.event
async def on_message(message):
    if message.content == "내정보":
        user = message.author
        date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22)+1420070400000)/1000)
        await message.channel.send(f"{message.author.mention}의 가입일 : {date.year}/{date.month}/{date.day}")
    if message.content.startswith("!인증"):
        msg_1 = message.content.split()
        try:
            data = msg_1[1]
        except:
            await message.channel.send("이메일을 입력해주세요")
            return
        a = random.randint(1000,9999)
        print(a)
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()      # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login('본인이메일', '본인이메일비밀번호')
        msg = MIMEText(str(a))
        msg['Subject'] = '메일제목'
        msg['To'] = data
        smtp.sendmail('본인이메일', data, msg.as_string())
        smtp.quit()
        await message.channel.send("해당이메일로 인증코드가 전송되었습니다 60초 이내에 인증번호를 보내주세요")
        try:
            msg2 = await client.wait_for('message', timeout=60)
        except asyncio.TimeoutError:
            await message.channel.send("30초가 지났어요 다시해주세요")
            return
        else:
            psg = str(msg2.content)
            print(psg)
            if psg == str(a):
                await message.channel.send("인증되었습니다")
                role = discord.utils.get(message.guild.roles, name="서버원")
                await message.author.add_roles(role)

client.run(token)
