from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.model import Friend
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import requests
import time
import os
import subprocess

channel = Channel.current()

async def download(url, name):
    # 下载链接中的文件
    r = requests.get(url)
    # 储存在相对路径..temp文件夹下，储存为pptx文件
    with open("temp/%s"%(name), "wb") as code:
        code.write(r.content)

async def convert_ppt_to_pdf(ppt_file_path):
    output_dir = os.path.dirname(ppt_file_path)
    command = ["soffice", "--headless", "--convert-to", "pdf", ppt_file_path, "--outdir", output_dir]
    subprocess.call(command)

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain,groupmessage: GroupMessage):
# 仅在群组 554568890 中响应
    if group.id == 554568890:
        # 如果消息内存在引用行为
        if groupmessage.quote != None and message.display == "1":
            try:
                m=await app.get_message_from_id(
                    groupmessage.quote.id,#找到引用的消息id
                    group
                )
                # 找到引用的消息
                m=await app.get_message_from_id(
                    groupmessage.quote.id,
                    group
                )
                # 如果引用的消息内存在文件
                if element.File in m.message_chain:
                    # 获取file.id
                    if files := m.message_chain.get(element.File):
                        file, = files

                    # 获取file.id的文件信息
                    fileinfo = await app.get_file_info(
                        target=group,
                        id=file.id,
                        with_download_info=True
                    )
                    # 捕获消息提示
                    await app.send_message(
                        group,
                        MessageChain("conversion start,filename=%s"%(fileinfo.name)),
                        quote=groupmessage.id
                    )
                    # 文件命名为时间戳
                    # fname=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
                    fname=fname=".".join(fileinfo.name.split(".")[0:-1])
                    await download(fileinfo.download_info.url,fname+".pptx")
                    await convert_ppt_to_pdf("temp/%s"%(fname+".pptx"))
                    await app.upload_file(
                        data=open("temp/%s.pdf"%(fname), "rb"),
                        target=group,
                        name=fname+".pdf",
                    )
                    # 清理temp文件夹
                    for files in os.listdir("temp"):
                        os.remove("temp/%s"%(files))
                    # 模块完成应答
                    await app.send_message(
                        group,
                        MessageChain("Conversion and cleanup complete"),
                        quote=groupmessage.id,
                    )
            except Exception as e:
                await app.send_message(
                    group,
                    MessageChain("error:"+str(e)),
                )
