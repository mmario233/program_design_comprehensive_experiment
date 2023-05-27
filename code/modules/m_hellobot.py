from typing import Optional
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.model import Friend
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.ariadne.util.interrupt import FunctionWaiter
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema


channel = Channel.current()


    
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain,groupmessage: GroupMessage):
    if message.display == "你好":
        await app.send_message(
            group,
            MessageChain(f"不要说{message.display}，早点睡觉"),
            quote=groupmessage.id,
        )
        # async def waiter(waiter_group:Group, waiter_message: MessageChain) -> Optional[str]:
        #     print("inside waiter")
        #     if waiter_group.id == 554568890:
        #         saying = waiter_message.display
        #     return saying
        # print("before wait")
        # result = await FunctionWaiter(waiter, [GroupMessage]).wait()  
        # print("after wait")
        # await app.send_message(
        #     group,
        #     MessageChain(result),
        #     quote=groupmessage.id,
        # )


# 测试返回图片功能
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain,groupmessage: GroupMessage):
    if message.display == "图片test":
        await app.send_message(
            group,
            MessageChain(element.Image(path='./capt.png')+element.Image(path='./capt.png')),
            quote=groupmessage.id,
        )

# 20230518新增未同步至服务器
# help
txt="[1.reminder：] @bot remind 任务 今天/明天/后天（日期） 时.分\n[2.课程表classadd：] @bot classadd 数学 N301 陈老师 8.00 9.00 1 20220301 20991231 steve\n"
txt1="[3.查询信息门户：] bupt信息门户\n[4.每日诗词：] @bot 诗词\n[5.天气：] @bot 天气\n[6.回声洞：] [获取].cave [发送].cave send author_name text"
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def bothelp(app: Ariadne, group: Group, message: MessageChain,groupmessage: GroupMessage):
    if message.display == "bot help ls":
        await app.send_message(
            group,
            MessageChain(txt+txt1),
            quote=groupmessage.id,
        )