from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.model import Friend
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()

# 由于Group有group与member，而friend只有friend，因此想要范式处理，需要Union

from typing import Union

import pymysql
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema
from .func_weather import weather
from .func_poem import poem
from .func_weather import savepath


# # 工作日每天7点30分30秒发送消息
# @channel.use(SchedulerSchema(timers.crontabify("30 7 * * 1,2,3,4,5 5")))
# async def goodmorning(app: Ariadne):
#     await app.send_group_message(
#         554568890,MessageChain("早上好")
#     )

# # weekend每天8点30分发送消息
# @channel.use(SchedulerSchema(timers.crontabify("30 8 * * 0,6 5")))
# async def goodmorning(app: Ariadne):
#     await app.send_group_message(
#         554568890,MessageChain("早上好")
#     )

# 每天00:00秒发送消息
@channel.use(SchedulerSchema(timers.crontabify("0 0 * * * 5")))
async def goodnight(app: Ariadne):
    await app.send_group_message(
        554568890,MessageChain("记得早点休息")
    )

group_id = 554568890

# 工作日每天7点30分30秒发送消息
@channel.use(SchedulerSchema(timers.crontabify("30 7 * * 1,2,3,4,5 5")))
async def goodmorning(app: Ariadne):
    info=weather("hourly")
    today_poem=poem()
    await app.send_group_message(
        group_id,MessageChain("早上好\n"+info["描述"]+element.Image(path="%s/qiwen_1d.png"%savepath)+element.Image(path="%s/shidu_1d.png"%savepath)+element.Image(path="%s/qiangdu_1d.png"%savepath))
    )
    await app.send_group_message(
        group_id,MessageChain(today_poem[0])
    )

# weekend每天8点30分发送消息
@channel.use(SchedulerSchema(timers.crontabify("30 8 * * 0,6 5")))
async def goodmorning(app: Ariadne):
    info=weather("hourly")
    today_poem=poem()
    await app.send_group_message(
        group_id,MessageChain("早上好\n"+info["描述"]+element.Image(path="%s/qiwen_1d.png"%savepath)+element.Image(path="%s/shidu_1d.png"%savepath)+element.Image(path="%s/qiangdu_1d.png"%savepath))
    )
    await app.send_group_message(
        group_id,MessageChain(today_poem[0])
    )