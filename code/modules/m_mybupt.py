from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.model import Friend
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.ariadne.message import Source
from graia.ariadne.util.interrupt import FunctionWaiter
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.scheduler.saya import SchedulerSchema
from graia.scheduler import timers

from typing import Optional, Union

import pymysql
import time


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
from PIL import Image

import os


channel = Channel.current()


# 采用以下来解决ssl证书错误
# 配置选项
options = webdriver.ChromeOptions()

# 设置打印机
settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isHeaderFooterEnabled": False,

        # "customMargins": {},
        #"marginsType": 2,#边距（2是最小值、0是默认）
        # "scaling": 100,
        # "scalingType": 3,
        # "scalingTypePdf": 3,
        #"isLandscapeEnabled": True,  # 若不设置该参数，默认值为纵向
        "isCssBackgroundEnabled": True,
        "mediaSize": {
            "height_microns": 297000,
            "name": "ISO_A4",
            "width_microns": 210000,
            "custom_display_name": "A4"
        },
    }

options.add_argument('--enable-print-browser')
options.add_argument('--headless')
    # options.add_argument('--headless') #headless模式下，浏览器窗口不可见，可提高效率
prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': '/root/bot/bupttemp/'  # 此处填写你希望文件保存的路径,可填写your file path默认下载地址
    }

options.add_argument('--kiosk-printing')  # 静默打印，无需用户点击打印页面的确定按钮
options.add_experimental_option('prefs', prefs)

# 忽略证书错误
options.add_argument('--ignore-certificate-errors')
# 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 忽略 DevTools listening on ws://127.0.0.1... 提示
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')





async def waiter(waiter_group:Group, waiter_message: MessageChain) -> Optional[str]:
    print("inside waiter")
    if waiter_group.id == 554568890:
        saying = waiter_message.display
        return saying

# 手动触发
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def mybupt(app: Ariadne, group: Group, message: MessageChain):
    if message.display=="bupt信息门户":
        await app.send_group_message(
                554568890,
                MessageChain("尝试登录中..."),
            )
        trytime=0
        vpnsuccess=0
        while trytime<3:
            try:
                # 获取驱动
                drive = webdriver.Chrome(options=options)
                # 以webvpn登录
                drive.get("https://webvpn.bupt.edu.cn/")
                # 登录webvpn
                username = drive.find_element(By.XPATH, "//*[@id='user_name']")
                username.send_keys("2021210405")
                password = drive.find_element(By.XPATH, "//*[@id='form']/div[3]/div/input")
                password.send_keys("123456")
                login=drive.find_element(By.XPATH,"//*[@id='login']")
                login.click()
                sleep(2)
                drive.switch_to.window(drive.window_handles[-1])
                await app.send_group_message(
                    554568890,
                    MessageChain("webvpn登陆成功"),
                )
                # 登录信息门户
                mybupt=drive.find_element(By.XPATH,"//*[@id='__layout']/div/div/div[3]/div/div[2]/div/div[1]/div/div[2]/div/div[1]")
                mybupt.click()
                sleep(0.5)
                drive.switch_to.window(drive.window_handles[-1])
                sleep(0.5)
                drive.switch_to.frame("loginIframe")
                # # 选择密码登录
                keyloginin=drive.find_element(By.XPATH,"//*[@id='content-title']/a[2]")
                keyloginin.click()
                vpnsuccess=1
                break
            except Exception as e:
                vpnsuccess=0
                drive.quit()
                await app.send_group_message(
                    554568890,
                    MessageChain("重新尝试登录webvpn..."+str(e)),
                )
                trytime+=1
                continue
        if vpnsuccess==1:
            ttime=0
            while ttime<2:
                try:
                    drive.find_element(By.XPATH,"//*[@id='captcha']/img").screenshot('capt.png')
                    await app.send_group_message(
                        554568890,
                        MessageChain("登录失败，请在两分钟内输入验证码"+element.Image(path="./capt.png")),
                    )
                    
                    print("before wait")
                    result = await FunctionWaiter(waiter, [GroupMessage]).wait()  
                    print("after wait")
                    idcode=drive.find_element(By.XPATH,"//*[@id='cptValue'] ")
                    idcode.send_keys(result)
                    username=drive.find_element(By.XPATH,"//*[@id='username']")
                    username.send_keys("2021210405")
                    password=drive.find_element(By.XPATH,"//*[@id='password']")
                    password.send_keys("123456")
                    login=drive.find_element(By.XPATH,"//*[@id='content-con']/div[2]/div[7]/input")
                    login.click()
                    sleep(1)
                    drive.switch_to.window(drive.window_handles[-1])
                    print("------------------------------------before tongzhi------------------------------")
                    # 点击校内通知
                    tongzhi=drive.find_element(By.XPATH,"/html/body/div[1]/div/ul/li[5]/a")
                    tongzhi.click()
                    success=1
                    await app.send_group_message(
                        554568890,
                        MessageChain("登录门户成功"),
                    )
                    break
                except:
                    try:
                        # 输入用户名密码
                        username=drive.find_element(By.XPATH,"//*[@id='username']")
                        username.send_keys("2021210405")
                        password=drive.find_element(By.XPATH,"//*[@id='password']")
                        password.send_keys("123456")
                        login=drive.find_element(By.XPATH,"//*[@id='content-con']/div[2]/div[7]/input")
                        login.click()
                        sleep(2)
                        drive.switch_to.window(drive.window_handles[-1])
                        # 点击校内通知
                        tongzhi=drive.find_element(By.XPATH,"/html/body/div[1]/div/ul/li[5]/a")
                        tongzhi.click()
                        success=1
                        await app.send_group_message(
                            554568890,
                            MessageChain("登录门户成功"),
                        )
                        break
                    except Exception as e:
                        ttime+=1
                        # drive.quit()
                        success=0
                        drive.switch_to.window(drive.window_handles[-1])
                        await app.send_group_message(
                            554568890,
                            MessageChain("重新尝试登录..."+str(e)),
                        )
                        sleep(1)
                        continue

        
        if success==1:
            filepath="/root/bot/webcat/webcat.txt"
            webcatfile=open(filepath,"r+",encoding="utf-8")
            lastlist=webcatfile.read()
            webcatfile.seek(0,0)
            print(lastlist)
            print("-----------------------------------------------------开始获取新通知--")
            await app.send_group_message(
                554568890,
                MessageChain("获取新通知..."),
            )
            # selectxpath="/html/body/print-preview-app//print-preview-sidebar//div[2]/print-preview-destination-settings//print-preview-destination-select//print-preview-settings-section/div/select"
            for i in range(1,11):
                tz=drive.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/ul/li["+str(i)+"]").text
                webcatfile.write(str(tz.encode("utf-8"))+'\n')
                # tzlist.append(drive.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/ul/li["+str(i)+"]").text)
                if str(tz.encode("utf-8")) not in str(lastlist):
                    # # 进入通知详情页
                    # drive.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/ul/li["+str(i)+"]").click()
                    # # 窗口切换
                    # drive.switch_to.window(drive.window_handles[-1])
                    # sleep(0.5)
                    # # js命令打印
                    # drive.execute_script('document.title="%s.pdf";window.print();'%(tz.split("\n")[0]))
                    # # 关闭当前通知窗口
                    # drive.close()
                    # # 窗口切换回列表页
                    # drive.switch_to.window(drive.window_handles[-1])
                    # # 歇会
                    # sleep(1)
                    await app.send_group_message(
                        554568890,
                        MessageChain("【新通知】"+tz.split("\n")[0]),
                    )


            webcatfile.close()
            drive.quit()
        #     await app.send_group_message(
        #         554568890,
        #         MessageChain("准备上传新通知..."),
        #     )
        #     print("-----------------------新通知获取完毕--------------------------------")
        # for files in os.listdir("/root/bot/bupttemp"):
        #     await app.upload_file(
        #                     data=open("/root/bot/bupttemp/%s"%(files), "rb"),
        #                     target=554568890,
        #                     name=files,
        #                 )
        await app.send_group_message(
                554568890,
                MessageChain("Done"),
            )
        


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def mybupt(app: Ariadne, group: Group, message: MessageChain,groupmessage: GroupMessage):
    if message.display=="clear bupttemp":
        for files in os.listdir("/root/bot/bupttemp"):
            os.remove("/root/bot/bupttemp/%s"%(files))
        await app.send_group_message(
                    554568890,
                    MessageChain("bupttemp清理成功"),
            )