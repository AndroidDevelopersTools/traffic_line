import requests
import json
import pandas as pd
"""
#0、在这里设置城市和线路名！(应确保有这条线路)
cityname='青岛'
line='110路'
total_dm = pd.DataFrame()
total_path = pd.DataFrame()
for i in range(1, 1000):
    line = str(i) + "路"
    url = 'https://restapi.amap.com/v3/bus/linename?s=rsv3&extensions=all&key=a5b7479db5b24fd68cedcf24f482c156&output=json&city={}&offset=1&keywords={}&platform=JS'.format(cityname,line)
    #1、获取数据
    r = requests.get(url).text
    rt = json.loads(r)
    #2、读取公交线路部分信息（可参考rt变量中的内容，按需获取）
    dt = {}

    dt['line_name'] = rt['buslines'][0]['name'] #公交线路名字
    dt['start_stop'] = rt['buslines'][0]['start_stop'] #始发站
    dt['end_stop'] = rt['buslines'][0]['end_stop'] #终点站
    #3、获取沿途站点站名和对应坐标并保存在“公交基本信息”表格中
    station_name = []
    station_coords = []
    for st in rt['buslines'][0]['busstops']:
        station_name.append(st['name'])
        station_coords.append(st['location'])
    dt['station_name'] = station_name
    dt['station_coords'] = station_coords
    dm = pd.DataFrame(dt)
    dm['latitude'], dm['longitude'] = dm['station_coords'].str.split(',', 1).str#将坐标拆解为经度和纬度
    total_dm = pd.concat([total_dm, dm], axis=0)
"""
"""
    #4、获取沿途路径坐标（行驶轨迹）并保存在“公交路线轨迹表格中”
    tmp={}
    polyline=rt['buslines'][0]['polyline']
    tmp['station_coords']=polyline.split(";")
    path=pd.DataFrame(tmp)
    path['latitude'], path['longitude'] = path['station_coords'].str.split(',', 1).str#将坐标拆解为经度和纬度
    total_path = pd.concat([total_path, path], axis=0)

total_dm.to_csv('公交基本信息.csv',encoding='utf-8-sig')
total_path.to_csv('公交路线轨迹.csv',encoding='utf-8-sig')
"""

def get_line(cityname, line, path):
    # 获取数据
    url = 'https://restapi.amap.com/v3/bus/linename?s=rsv3&extensions=all&key=a5b7479db5b24fd68cedcf24f482c156&output=json&city={}&offset=1&keywords={}&platform=JS'.format(
        cityname, line)
    r = requests.get(url).text
    rt = json.loads(r)
    try:  # 若报错（即该没有线路）进入except,跳过
        polyline = rt['buslines'][0]['polyline']  # 获取沿途路径坐标
        path = path + polyline  # 这里通过path字符串累计获取所有公交线路路径
        return path
    except:
        print('没有{}路公交'.format(line))
        print("------")
        return path
        pass


# 获取公交基本信息
def get_station(cityname, line):
    global bus_num
    # 1、获取当前公交线路数据
    url = 'https://restapi.amap.com/v3/bus/linename?s=rsv3&extensions=all&key=a5b7479db5b24fd68cedcf24f482c156&output=json&city={}&offset=1&keywords={}&platform=JS'.format(
        cityname, line)
    r = requests.get(url).text
    rt = json.loads(r)
    try:
        # 2、读取当前公交线路主要信息
        # 2、读取当前公交线路主要信息
        dt = {}
        dt['line_name'] = rt['buslines'][0]['name']  # 公交线路名字
        dt['start_stop'] = rt['buslines'][0]['start_stop']  # 始发站
        dt['end_stop'] = rt['buslines'][0]['end_stop']  # 终点站
        dt['bounds'] = rt['buslines'][0]['bounds']  # 行车区间（非始发站，终点站坐标）
        dt['distance'] = rt['buslines'][0]['distance']  # 全程长度

        # 3、获取沿途站点站名、对应坐标和“第几站”信息
        station_name = []
        station_coords = []
        station_sequence = []
        for st in rt['buslines'][0]['busstops']:
            station_name.append(st['name'])
            station_coords.append(st['location'])
            station_sequence.append(st['sequence'])

        dt['station_name'] = station_name  # 沿途站点名
        dt['station_coords'] = station_coords  # 沿途站点坐标
        dt['station_sequence'] = station_sequence  # 沿途站点第几站
        bus_num += 1  # 有效公交数+1
        return pd.DataFrame(dt)  # 返回pd.DataFrame()类型

    except:
        print('没有{}公交'.format(line))  # 输出没有的公交线路名字，可省略
        return pd.DataFrame([])  # 返回空的pd.DataFrame类型


# 获取当前城市所有公交基本信息：线路名、行车区间、全程长度、沿途站点及坐标






if __name__ == "__main__":
    path_str = ''
    bus_num = 0
    all_bus = pd.DataFrame()
    for i in range(1, 1000):
        path_str = get_line('潍坊', str(i), path_str)
        all_bus = pd.concat([all_bus, get_station('潍坊', str(i) + '路')])
    print(len(path_str))  # 获取坐标字符串总长度（不是坐标总数，总数大约为这个数/21）
    path = {}
    path['station_coords'] = path_str.split(";")  # 通过";"拆分每个路径坐标
    path = pd.DataFrame(path)
    # 将坐标拆解为经度longitude,和纬度latitude（请根据具体使用场景处理数据）
    path['longitude'], path['latitude'] = path['station_coords'].str.split(',', 1).str
    # path.to_csv('潍坊1000条线路公交路线轨迹数据.csv', encoding='utf-8')
    # path.iloc[0:20000, :].to_csv('wf1.csv', encoding='utf-8')
    # path.iloc[20000:40000, :].to_csv('wf2.csv', encoding='utf-8')
    # path.iloc[40000: , :].to_csv('wf3.csv', encoding='utf-8')
    # path.drop(['station_coords'],axis=1,inplace=True)  #狡兔死走狗烹，飞鸟尽良弓藏  经度，纬度提取出来，可以把原来的经纬度给删了
    path.to_csv('青岛10条线路公交路线轨迹数据.csv',index=False,encoding='utf-8-sig')  #index=False即不显示index索引
    # print("Bus_info函数遍历{}前{}路公交,有效公交线路数为：{}个".format('青岛', for_num, bus_num))
    all_bus.to_csv("{}前{}路公交(有效线路数：{})基本信息.csv".format('潍坊', '1000', bus_num), encoding='utf-8-sig')

