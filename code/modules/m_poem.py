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
from .func_poem import poem


channel = Channel.current()


# @bot 诗词
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def today_poem(app: Ariadne, group: Group, message: MessageChain,groupmessage: GroupMessage):
    if element.At(app.account)in message:
        if "诗词" in message.display:
            txt=poem()
            await app.send_message(
                group,
                MessageChain(txt[1]+txt[2]),
                quote=groupmessage.id,
            )
