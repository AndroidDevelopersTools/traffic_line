import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import tensorflow as tf

myDataset = pd.read_csv("bus_infomation.csv", header=0, error_bad_lines=False, na_values ="?", comment='\t', sep=",", skipinitialspace=True)
myDataset_1 = pd.read_csv("bus_info_wf.csv", header=0, error_bad_lines=False, na_values ="?", comment='\t', sep=",", skipinitialspace=True)
# pd.read_excel()
# nodes = myDataset.loc[:, 'station_name'].values
index = myDataset.iloc[:, 0].values

print(index)
index_1 = myDataset_1.iloc[:, 0].values
# print(max(index_1))
myList = []
myList_1 = []
# print(len(index))
begin = 0
while begin < len(index):
    for i in range(77):
        try:
            if index[begin + i + 1] < index[begin + i]:
                nodes = myDataset.loc[begin:begin + i + 1, 'station_name'].values
                begin = begin + i + 1
                myList.append(nodes)
                i = 0
        except:
            nodes = myDataset.loc[begin:begin + i + 1, 'station_name'].values
            begin = begin + i + 1
            myList.append(nodes)
            break

# 潍坊
begin = 0
while begin < len(index_1):
    for i in range(97):
        try:
            if index_1[begin + i + 1] < index_1[begin + i]:
                nodes = myDataset_1.loc[begin:begin + i + 1, 'station_name'].values
                begin = begin + i + 1
                myList_1.append(nodes)
                i = 0
        except:
            nodes = myDataset_1.loc[begin:begin + i + 1, 'station_name'].values
            begin = begin + i + 1
            myList_1.append(nodes)
            break







# 构造地图
# G = nx.MultiGraph()
G = nx.Graph()
G_1 = nx.Graph()
for i in range(427):
    try:
        H = nx.path_graph(myList[i])
        G.add_nodes_from(H)
        G.add_edges_from(H.edges())
    except:
        break


for i in  range(140):
    try:
        H = nx.path_graph(myList_1[i])
        G_1.add_nodes_from(H)
        G_1.add_edges_from(H.edges())
    except:
        break


# 绘制地图
nx.draw(G, with_labels=True)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.show()
# plt.savefig('map.PNG')

nx.draw(G_1, with_labels=True)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.show()



# 聚类系数
network_clustering = 0
all_nodes_clustering = nx.clustering(G)
for k, v in all_nodes_clustering.items():
    network_clustering += v
print("青岛聚类系数：")
print(network_clustering/len(all_nodes_clustering))

network_clustering = 0
all_nodes_clustering = nx.clustering(G_1)
for k, v in all_nodes_clustering.items():
    network_clustering += v
print("潍坊聚类系数：")
print(network_clustering/len(all_nodes_clustering))



# 平均路径长度
print("青岛平均路径长度：")
print(nx.average_shortest_path_length(G))

print("潍坊平均路径长度：")
print(nx.average_shortest_path_length(G_1))





# 度分布
degree = nx.degree_histogram(G)
degree_1 = nx.degree_histogram(G_1)

# print(len(degree))
# print(degree)
# print(len(degree_1))
# print(degree_1)

plt.subplot(1,2,1)
x = range(len(degree))
y = [z for z in degree]
plt.plot(x,y,color="blue",linewidth=2)
plt.title('青岛度分布',fontsize=12,weight='bold',loc='center')
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

plt.subplot(1,2,2)
x_1 = range(len(degree_1))
y_1 = [z for z in degree_1]
plt.plot(x_1,y_1,color="red",linewidth=2)
plt.title('潍坊度分布',fontsize=12,weight='bold',loc='center')
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

plt.show()

