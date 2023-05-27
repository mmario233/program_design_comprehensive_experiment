import requests
import urllib
import json
import hashlib
import uuid
import time
import sys
import matplotlib.pyplot as plt
import matplotlib
import re
# savepath='./weatherpngtemp/' # 保存图片的路径（本地windows）
savepath='/root/bot/weatherpng/' # 保存图片的路径（服务器）
# 设置绘图中文样式
font = {'family': 'MicroSoft YaHei',
        'weight': 'bold',
        'size': 12}
matplotlib.rc('font', **font)
MAX_RETRY = 3

def plot_list(lst, pattern):
    plt.clf()
    if pattern == 'precipitation_2h':
        plt.plot(lst)
        plt.title('近两小时的降水强度预测')
        plt.xlabel('分钟/min')
        plt.ylabel('降水强度')
        x_label = ['{}'.format(i,) for i in range(0, len(lst)+1, 5)]
        # print(range(0, len(list)+1, 5))
        plt.xticks(range(0, len(lst)+1, 5), x_label, rotation=45)
        plt.yticks(range(int(max(lst))+10))
        fig = plt.gcf()
        fig.savefig(savepath+'jiangshui_2h.png')
    elif pattern == 'probability':
        plt.plot(range(30, 121, 30), lst)
        plt.title('近两小时的降水概率预测')
        plt.xlabel('分钟/min')
        plt.ylabel('降水概率')
        x_label = ['{}'.format(i, ) for i in range(0, 121, 30)]
        # print(range(0, len(list)+1, 5))
        plt.xticks(range(0, 121, 30), x_label)
        plt.yticks(range(int(max(lst)) + 3))
        fig = plt.gcf()
        fig.savefig(savepath+'gailv_2h.png')
    elif pattern == 'precipitation':
        datetime = []
        value = []
        for item in lst:
            time = re.search('.*T(.*)\+.*', item['datetime'])
            datetime.append(time.group(1))
            value.append(item['value'])
        plt.plot(value)
        plt.title('近一天的降水强度预测')
        plt.xlabel('时刻/小时')
        plt.ylabel('降水概率')
        x_label = ['{}'.format(i, ) for i in datetime]
        plt.xticks(range(len(lst)), x_label, rotation=45)
        fig = plt.gcf()
        fig.savefig(savepath+'qiangdu_1d.png')
    elif pattern == 'temperature':
        datetime = []
        value = []
        for item in lst:
            time = re.search('.*T(.*)\+.*', item['datetime'])
            datetime.append(time.group(1))
            value.append(item['value'])
        plt.plot(value)
        plt.title('近一天的温度预测')
        plt.xlabel('时刻/小时')
        plt.ylabel('摄氏度/℃')
        x_label = ['{}'.format(i, ) for i in datetime]
        plt.xticks(range(len(lst)), x_label, rotation=45)
        fig = plt.gcf()
        fig.savefig(savepath+'qiwen_1d.png')
    elif pattern == 'humidity':
        datetime = []
        value = []
        for item in lst:
            time = re.search('.*T(.*)\+.*', item['datetime'])
            datetime.append(time.group(1))
            value.append(100*item['value'])
        plt.plot(value)
        plt.title('近一天的湿度预测')
        plt.xlabel('时刻/小时')
        plt.ylabel('百分比/%')
        x_label = ['{}'.format(i, ) for i in datetime]
        plt.xticks(range(len(lst)), x_label, rotation=45)
        fig = plt.gcf()
        fig.savefig(savepath+'shidu_1d.png')
    return fig



# 需要提供是否实时天气还是天气预报
# 如果是天气预报需要知道单位为分钟、小时或天
# 分钟级预报 返回的近两小时内的降水强度和降水概率
#
def weather(way):
    Token = "AqXFEo9wI0o6iFG9"
    latitude = "40.164"
    longitude = "116.295"
    url = "https://api.caiyunapp.com/v2.5/%s/%s,%s/%s.json" % (Token, longitude, latitude, way)
    print(url)
    if way == "realtime":
        retry_times = 0
        while retry_times <= MAX_RETRY:
            try:
                res = requests.get(url, timeout=3)
                res_json = json.loads(res.text)
                data = res_json['result']['realtime']
                res_content = '当前温度为%d摄氏度，湿度为%d%%，空气质量%s，污染指数为%d。' % (
                                data['temperature'], data['humidity'] * 100,
                                data['air_quality']['description']['chn'],
                                data['air_quality']['aqi']['chn'])
                break
            except Exception:
                print('err')
                retry_times += 1
                time.sleep(retry_times ** 2)
                continue
        print([res_content])
        # 返回一个列表 字符串
        return [res_content]
    elif way == "minutely":
        retry_times = 0
        while retry_times <= MAX_RETRY:
            try:
                res = requests.get(url, timeout=3)
                res_json = json.loads(res.text)
                data = res_json['result']['minutely']
                # print(data)
                data_min = {'描述': data['description']}
                precipitation_2h = plot_list(data['precipitation_2h'], 'precipitation_2h')
                data_min['降水强度'] = precipitation_2h
                probability = plot_list(data['probability'], 'probability')
                data_min['降水概率'] = probability
                break
            except Exception:
                print('err')
                retry_times += 1
                time.sleep(retry_times ** 2)
                continue
        precipitation_2h.show()
        print(data_min)
        #  返回一个对象，一个描述的字符串和两个关于降水的图
        return data_min
    elif way == "hourly":
        retry_times = 0
        while retry_times <= MAX_RETRY:
            try:
                res = requests.get(url + "?hourlysteps=24", timeout=3)
                res_json = json.loads(res.text)
                data = res_json['result']['hourly']
                print(data)
                data_hr = {'描述': data['description']}
                precipitation = plot_list(data['precipitation'], 'precipitation')
                data_hr['降水强度'] = precipitation
                temperature = plot_list(data['temperature'], 'temperature')
                data_hr['温度'] = temperature
                humidity = plot_list(data['humidity'], 'humidity')
                data_hr['湿度'] = humidity
                print(data_hr)
                break
            except Exception:
                print('err')
                retry_times += 1
                time.sleep(retry_times ** 2)
                continue
        return data_hr
    else:
        return "err"
    

weather("realtime")