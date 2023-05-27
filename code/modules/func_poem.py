import requests
import urllib
import json



# 每日古诗词，返回诗句和源诗
def poem():
    Token = "d+ee8ff8t54Km8BNCnkflzaq/cyHbcKN"
    url = 'https://v2.jinrishici.com/sentence'
    Headers = {
       'X-User-Token': "9OZE26qpfw1P2iWiygsFNixdURN3wO7c"
    }
    req = urllib.request.Request(headers=Headers, url=url)
    res = urllib.request.urlopen(req, timeout=3)
    if res.status == 200:
        text = res.read().decode('utf-8')
        txt = json.loads(text)
        if txt['status'] == "success":
            # print(txt['data']['content'])
            head = str(txt['data']['origin']['title']) + '\n' + str(txt['data']['origin']['dynasty']) + " " + str(txt['data']['origin']['author']) + '\n'
            content = ""
            for item in txt['data']['origin']['content']:
                if txt['data']['origin']['content'].index(item):
                    content += "\n"
                content += str(item)
            # 返回一个列表 包含每日一句， 源诗的头（标题、朝代和作者）， 源诗全文
            return [txt['data']['content'], head, content]
        else:
            return "err"
    else:
        print("请求失败，请检查网络后重试")
        return "err"

