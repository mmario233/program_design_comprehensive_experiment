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
channel = Channel.current()


# 添加字段
@channel.use(ListenerSchema(listening_events=[GroupMessage,FriendMessage]))
async def classadd(app: Ariadne,sender : Union[Group,Friend],message: MessageChain,source: Source):
    if element.At(app.account)in message:
        if "classadd" in message.display:
            db=pymysql.connect(
                host='38.114.186.213',
                user='root',
                password='123456',
                database='qqbot'
            )
            cur=db.cursor()
            try:
                sql="select class from classschedule"
                cur.execute(sql)
                result=cur.fetchall()
                classlist=[]
                for row in result:
                    classlist.append(row[0])
            except:
                db.rollback()
            data=message.display.split("classadd ")[1]
            if data in classlist:
                await app.send_message(
                    sender,
                    MessageChain("class is already appeared🏫"),
                    quote=source.id
                )
            else:
                if data.count(' ')!=8:
                    await app.send_message(
                        sender,
                        MessageChain("format is illegal"),
                        quote=source.id
                    )
                else:
                    # 样例输入：classadd 数学 1-1 陈老师 8.00 9.00 1 20220301 20991231 py
                    sqladd="insert into classschedule (class,room,teacher,begintime,endtime,weekday,begindate,enddate,owner) values ('%s');"%(data.replace(' ','\',\''))
                    try:
                        # 星期合法检查
                        if int(data.split(' ')[5])<0 or int(data.split(' ')[5])>7:
                            raise Exception("weekday illegal %s"%(data.split(' ')[5]))
                        # 时间合法检查
                        if int(data.split(' ')[3].split('.')[0])>23 or int(data.split(' ')[3].split('.')[0])<0 or int(data.split(' ')[3].split('.')[1])<0 or int(data.split(' ')[3].split('.')[1])>59:
                            raise Exception("begintime illegal %s"%(data.split(' ')[3]))
                        if int(data.split(' ')[4].split('.')[0])>23 or int(data.split(' ')[4].split('.')[0])<0 or int(data.split(' ')[4].split('.')[1])<0 or int(data.split(' ')[4].split('.')[1])>59:
                            raise Exception("endtime illegal %s"%(data.split(' ')[4]))
                        # 有效日期合法检查
                        if int(data.split(' ')[6])>20990000 or int(data.split(' ')[6])<20220301:
                            raise Exception("begindate illegal %s"%(data.split(' ')[6]))
                        if int(data.split(' ')[7])>20990000 or int(data.split(' ')[7])<20220301:
                            raise Exception("enddate illegal %s"%(data.split(' ')[7]))
                        
                        cur.execute(sqladd)
                        db.commit()
                        await app.send_message(
                            sender,
                            MessageChain("classadd successfully🏫"),
                            quote=source.id
                        )
                    except Exception as err:
                        db.rollback()
                        await app.send_message(
                            sender,
                            MessageChain("%s"%(err)),
                            quote=source.id
                        )
                    except:
                        db.rollback()
                        await app.send_message(
                            sender,
                            MessageChain("some errors ocurred"),
                            quote=source.id
                        )
            db.close()





@channel.use(SchedulerSchema(timers.crontabify("* * * * * 7")))
async def classreminder(app: Ariadne):
    db=pymysql.connect(
        host='38.114.186.213',
        user='root',
        password='123456',
        database='qqbot'
    )

    cur=db.cursor()

    sql="select * from classschedule"

    try:
        cur.execute(sql)
        result=cur.fetchall()
        classlist=[]
        for row in result:
            classlist.append(row)
    except:
        db.rollback()
    db.close()
    localtime=time.strftime("%w %H.%M %b %d %Y", time.localtime())
    localdate=int(time.strftime("%Y%m%d", time.localtime()))
    for classes in classlist:
        # 查询本工作日下课程
        if int(localtime[0])==classes[5]:
            # 判断课程是否处于有效期
            if int(classes[6])<=localdate and localdate<=int(classes[7]):
                # 判断课前30min提醒
                if int(localtime.split(' ')[1].replace('.',''))+30==int(classes[3].replace('.','')):
                    await app.send_group_message(
                            554568890,MessageChain("课程提醒(%s)\n 课程：%s \n 教室：%s \n 教师：%s \n 上课时间：%s --> %s"%(classes[8],classes[0],classes[1],classes[2],classes[3],classes[4]))
                        )
                # 以下仅作调试
                # else:
                #     await app.send_group_message(
                #             554568890,MessageChain("noclass(test)")
                #         )
                # 
        # 
        # else:
        #     await app.send_group_message(
        #             554568890,MessageChain("noclass(test1)")
        #         )
        # 以上仅作调试


