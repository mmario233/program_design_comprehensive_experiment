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
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema
from typing import Union
import pymysql

channel = Channel.current()

# 监测事件添加
# @bot remind 任务 今天/明天/后天（日期） 时.分
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def remind(app: Ariadne, group: Group,message: MessageChain):
    if element.At(app.account) in message:
        if "remind" in message.display:
            db=pymysql.connect(
                host='38.114.186.213',
                user='root',
                password='123456',
                database='qqbot'
            )
            cur=db.cursor()
            try:
                sql="select * from remindlist"
                cur.execute(sql)
                result=cur.fetchall()
                tasklist=[]
                for row in result:
                    tasklist.append(row)
                print(tasklist)
            except:
                db.rollback()
            # data=input("input:")
            data=message.display.split("remind ")[1]
            #任务 今天/明天/后天（日期） 时.分
            # print(len(data.split(' ')))
            if len(data.split(' '))<2:
                # print("-----------check begin------------------")
                try:
                    if data.split(' ')[1]=="今天":
                        if int(time.strftime("%H", time.localtime(time.time())))>12:
                            raise Exception("it is already afternoon today,please input time after 12:00(default is 12:00)")
                        else:
                            # 获取今天日期
                            remindtime=time.strftime("%Y%m%d", time.localtime(time.time()))+"12.00"
                    elif data.split(' ')[1]=="明天":
                        # 获取明天日期
                        remindtime=time.strftime("%Y%m%d", time.localtime(time.time() + 24 * 60 * 60))+"12.00"
                    elif data.split(' ')[1]=="后天":
                        # 获取后天日期
                        remindtime=time.strftime("%Y%m%d", time.localtime(time.time() + 24 * 60 * 60 * 2))+"12.00"
                    else:
                        # 日期合法性检查
                        if int(data.split(' ')[1].replace('.',''))<int(time.strftime("%Y%m%d", time.localtime(time.time()))):
                            raise Exception("date error %s"%(data.split(' ')[1]))
                        # 时间合法性检查
                        elif int(data.split(' ')[1].replace('.',''))==int(time.strftime("%Y%m%d", time.localtime(time.time()))):
                            if int(data.split(' ')[2].split('.')[0])<int(time.strftime("%H", time.localtime(time.time()))) or (int(data.split(' ')[2].split('.')[0])==int(time.strftime("%H", time.localtime(time.time()))) and int(data.split(' ')[2].split('.')[1])<int(time.strftime("%M", time.localtime(time.time())))):
                                raise Exception("time error %s"%(data.split(' ')[2]))
                        elif int(data.split(' ')[2].split('.')[0])>23 or int(data.split(' ')[2].split('.')[0])<0 or int(data.split(' ')[2].split('.')[1])<0 or int(data.split(' ')[2].split('.')[1])>59:
                            raise Exception("time error %s"%(data.split(' ')[2]))
                        else:
                            remindtime=data.split(' ')[1].replace('.','')+" "+data.split(' ')[2]
                    print("remindtime:",remindtime+"  check done")
                    for task in tasklist:
                        if data.split(' ')[0]==task[2] and remindtime==task[3]:
                            raise Exception("task is already appeared")
                    text=str(1234567)+"-"+"group=name"+"-"+data.split(' ')[0]+"-"+remindtime
                    sqladd="insert into remindlist (groupnum,idname,tasks,remindtime) values ('%s');"%(text.replace("-",'\',\''))
                    cur.execute(sqladd)
                    db.commit()

                except Exception as e:
                    db.rollback()
                    await app.send_group_message(
                            554568890,MessageChain(e)
                        )
            else:
                # print("-----------check begin------------------")
                try:
                    if data.split(' ')[1]=="今天":
                        if int(data.split(' ')[2].split('.')[0])<int(time.strftime("%H", time.localtime(time.time()))) or (int(data.split(' ')[2].split('.')[0])==int(time.strftime("%H", time.localtime(time.time()))) and int(data.split(' ')[2].split('.')[1])<int(time.strftime("%M", time.localtime(time.time())))):
                            raise Exception("time error %s"%(data.split(' ')[2]))
                        else:
                            # 获取今天日期
                            remindtime=time.strftime("%Y%m%d", time.localtime(time.time()))+" "+data.split(' ')[2]
                    elif data.split(' ')[1]=="明天":
                        if int(data.split(' ')[2].split('.')[0])>23 or int(data.split(' ')[2].split('.')[0])<0 or int(data.split(' ')[2].split('.')[1])<0 or int(data.split(' ')[2].split('.')[1])>59:
                            raise Exception("time error %s"%(data.split(' ')[2]))
                        # 获取明天日期
                        remindtime=time.strftime("%Y%m%d", time.localtime(time.time() + 24 * 60 * 60))+" "+data.split(' ')[2]
                    elif data.split(' ')[1]=="后天":
                        if int(data.split(' ')[2].split('.')[0])>23 or int(data.split(' ')[2].split('.')[0])<0 or int(data.split(' ')[2].split('.')[1])<0 or int(data.split(' ')[2].split('.')[1])>59:
                            raise Exception("time error %s"%(data.split(' ')[2]))
                        # 获取后天日期
                        remindtime=time.strftime("%Y%m%d", time.localtime(time.time() + 24 * 60 * 60 * 2))+" "+data.split(' ')[2]
                    else:
                        # 日期合法性检查
                        if int(data.split(' ')[1].replace('.',''))<int(time.strftime("%Y%m%d", time.localtime(time.time()))):
                            raise Exception("date error %s"%(data.split(' ')[1]))
                        # 时间合法性检查
                        elif int(data.split(' ')[1].replace('.',''))==int(time.strftime("%Y%m%d", time.localtime(time.time()))):
                            if int(data.split(' ')[2].split('.')[0])<int(time.strftime("%H", time.localtime(time.time()))) or (int(data.split(' ')[2].split('.')[0])==int(time.strftime("%H", time.localtime(time.time()))) and int(data.split(' ')[2].split('.')[1])<int(time.strftime("%M", time.localtime(time.time())))):
                                raise Exception("time error %s"%(data.split(' ')[2]))
                        elif int(data.split(' ')[2].split('.')[0])>23 or int(data.split(' ')[2].split('.')[0])<0 or int(data.split(' ')[2].split('.')[1])<0 or int(data.split(' ')[2].split('.')[1])>59:
                            raise Exception("time error %s"%(data.split(' ')[2]))
                        else:
                            remindtime=data.split(' ')[1].replace('.','')+" "+data.split(' ')[2]
                    # print("remindtime:",remindtime+"  check done")
                    for task in tasklist:
                        if data.split(' ')[0]==task[2] and remindtime==task[3]:
                            raise Exception("task is already appeared")
                    text=str(1234567)+"-"+"group=name"+"-"+data.split(' ')[0]+"-"+remindtime
                    sqladd="insert into remindlist (groupnum,idname,tasks,remindtime) values ('%s');"%(text.replace("-",'\',\''))
                    # print(sqladd)
                    cur.execute(sqladd)
                    db.commit()

                except Exception as e:
                    db.rollback()
                    await app.send_group_message(
                            554568890,MessageChain(e)
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

    sql="select * from remindlist"

    try:
        cur.execute(sql)
        result=cur.fetchall()
        tasklist=[]
        for row in result:
            tasklist.append(row)
    except:
        db.rollback()
    db.close()
    localtime=time.strftime("%w %H.%M %b %d %Y", time.localtime())
    localdate=int(time.strftime("%Y%m%d", time.localtime()))
    # print(localtime)
    # print(localdate)
    for task in tasklist:
        # 查询本工作日下课程
        # print(task[3].split(' ')[0])
        if int(localdate)==int(task[3].split(' ')[0]):
            if int(str(int(localtime.split(' ')[1].replace('.',''))+30)[2])>=6:
                localtime.split(' ')[1].replace('.','')[1]=str(int(localtime.split(' ')[1].replace('.','')[1])+1)
                localtime.split(' ')[1].replace('.','')[2]=str(int(localtime.split(' ')[1].replace('.','')[2])-6)
            if int(localtime.split(' ')[1].replace('.',''))+30 == int(task[3].split(' ')[1].replace('.','')):
                await app.send_group_message(
                        554568890,MessageChain("提醒事项：%s\n时间：%s\n"%(task[2],task[3]))
                    )