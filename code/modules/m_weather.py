import datetime
import time
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.model import Friend
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from typing import Union
import pymysql
import os
from .func_weather import weather
from .func_weather import savepath


channel = Channel.current()


# @bot 天气
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def today_weather(app: Ariadne, group: Group, message: MessageChain,groupmessage: GroupMessage):
    if element.At(app.account)in message:
        if "天气" in message.display:
            txt=weather("realtime")
            await app.send_message(
                group,
                MessageChain(txt[0]),
                quote=groupmessage.id,
            )
            info=weather("minutely")
            await app.send_message(
                group,
                MessageChain(info["描述"]+element.Image(path="%s/gailv_2h.png"%savepath)+element.Image(path="%s/jiangshui_2h.png"%savepath)),
                quote=groupmessage.id,
            )
