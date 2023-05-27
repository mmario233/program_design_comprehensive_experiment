from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.model import Friend
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.ariadne.message import Source


from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from typing import Union

import pymysql
import time
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema
import random

channel = Channel.current()

# .cave send name "message"

# sql="insert into qqbot.echo_cave (num,author,sound) values (0,'%s','%s');"%(name,data)

# 匿名替代名单
namelist=["不愿透露姓名的留声者","天外之音"]

# 添加字段
@channel.use(ListenerSchema(listening_events=[GroupMessage,FriendMessage]))
async def cave(app: Ariadne,sender : Union[Group,Friend],message: MessageChain,source: Source):
    if ".cave send" in message.display:
        data=message.display.split(".cave send ")[1]
        if data.count(" ")==0 or data.split(" ")[0] in ["None","none","NONE","匿名","无名","佚名"]:
            name=random.choice(namelist)
        else:
            name=data.split(" ")[0]
        data=data.split(' ')[1]
        db=pymysql.connect(
                host='38.114.186.213',
                user='root',
                password='123456',
                database='qqbot'
            )
        cur=db.cursor()
        try:
            sql="insert into qqbot.echo_cave (num,author,sound) values (0,'%s','%s');"%(name,data)
            cur.execute(sql)
            db.commit()
            await app.send_message(
                sender,
                MessageChain("send success"),
                quote=source.id
            )
        except Exception as e:
            db.rollback()
            await app.send_message(
                sender,
                MessageChain("send failed"),
                quote=source.id
            )
        db.close()




# 随机算法获得抽取的声音号
# num=2
# 获取字段
@channel.use(ListenerSchema(listening_events=[GroupMessage,FriendMessage]))
async def cave(app: Ariadne,sender : Union[Group,Friend],message: MessageChain,source: Source):
    if ".cave" == message.display:
        db=pymysql.connect(
                host='38.114.186.213',
                user='root',
                password='123456',
                database='qqbot'
            )
        cur=db.cursor()
        try:
            sql="select * from qqbot.echo_cave order by RAND() LIMIT 1"
            # sqlupdate="update qqbot.echo_cave set asktimes=asktimes+1 where num=%d"%(num)
            # 获取一条
            cur.execute(sql)
            result=cur.fetchall()
            tasklist=[]
            for row in result:
                tasklist.append(row)
            # 格式调整
            databack=tasklist[0][2]+"\n"+"\n"+"————————"+tasklist[0][1]
            await app.send_message(
                sender,
                MessageChain(databack),
                quote=source.id
            )
            # 更新访问次数
            # cur.execute(sqlupdate)
            # db.commit()
        except Exception as e:
            db.rollback()
            await app.send_message(
                sender,
                MessageChain("send failed"+e),
                quote=source.id
            )
        db.close()