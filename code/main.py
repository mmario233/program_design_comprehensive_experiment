import pkgutil #  python包管理

from creart import create
from graia.ariadne.app import Ariadne # 访问协议
from graia.ariadne.connection.config import ( # 网络协议配置
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.ariadne.event.message import GroupMessage # 群消息
from graia.ariadne.message.chain import MessageChain # 消息链
from graia.ariadne.model import Group
from graia.broadcast import Broadcast
from graia.ariadne.event.mirai import NudgeEvent

from graia.saya import Saya #  saya模块管理工具
import modules #  模块文件夹

saya = create(Saya)
app = Ariadne(
    connection=config(
        2092530065,  # 机器人的 qq 号
        "codecrafters",  #  mirai-api-http 中的 verifyKey
        #  mirai-api-http 地址中的地址与端口
        HttpClientConfig(host="http://localhost:9090"),
        WebsocketClientConfig(host="http://localhost:9090"),
        # 服务器端口如下
        # HttpClientConfig(host="http://172.25.24.100:9090"),
        # WebsocketClientConfig(host="http://172.25.24.100:9090"),
    ),
)

# 遍历modules中的模块，并以saya导入
with saya.module_context():
    for module_info in pkgutil.iter_modules(modules.__path__,modules.__name__+'.'):
        if module_info.name.split('.')[1].split('_')[0]=='m':
            saya.require(f"{module_info.name}") #  生成module_info.name为modules.hellobot。指定为modules文件夹内的hellobot模块


app.launch_blocking()
