#想定最大プロセス数10

#branch_output_dot

from platform import node
from graphviz import Graph
from graphviz import Digraph
import re

start_node_list = [] #開始ノードを格納するためのリスト
current_id_list = [] #intlist
snl_index = 0
node_id = 0
seq_num = 1
proc_comp = None #比較用の文字列格納用変数

g = Graph(format = "pdf")
dg = Digraph(format = "pdf")


f = open("result_simu.txt", "r")
line = f.readline()

while(line):    #ログを一行ずつ解析
    start = line.find("Starting")
    root = line.find("root")

    if start != -1:     #プロセスを開始させる時
        index = line.find("pid")
        pid = line[index:]
        start_node_list += pid
        g.node(str(node_id),pid)
        current_id_list += node_id
        node_id += 1
    elif root != -1:        #アクティブなプロセスが立ち上がる時
        index_mo = re.search(r'[p][r][o][c]\s\s[0-9]', line)
        mo_start = index_mo.start()
        proc = line[mo_start:mo_start+7]
        start_node_list += [proc]
        g.node(str(node_id),proc)    #node(ID:Label)
        current_id_list += [node_id]
        node_id += 1
    else:
        index_mo = re.search(r'[p][r][o][c]\s\s[0-9]', line)
        if index_mo != None:
            mo_start = index_mo.start()
            proc_comp = line[mo_start:mo_start+7]
            # print(proc_comp)
            if proc_comp in start_node_list:
                snl_index = start_node_list.index(proc_comp)
                g.node(str(node_id), str(seq_num))
                g.edge(str(current_id_list[snl_index]), str(node_id))
                current_id_list[snl_index] = node_id
                node_id += 1
                seq_num += 1
        elif index_mo == None:
            break


    line = f.readline()

f.close()
print(start_node_list)
print(current_id_list)
g.view()