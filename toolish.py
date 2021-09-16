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
rootnode_xpos = 0 #ルートノードのx座標を保持する変数
node_pos_list = []
num_proc = 0 #生成したプロセス数

fw = open("sequence.dot", "w")
f = open("result_simu.txt", "r")

fw.write("digraph sequence{\n")

line = f.readline()

while(line):    #ログを一行ずつ解析
    start = line.find("Starting")
    root = line.find("root")

    if start != -1:     #プロセスを開始させる時
        index = line.find("pid")
        pid = line[index:]
        start_node_list += pid
        current_id_list += node_id
        node_id += 1
    elif root != -1:        #アクティブなプロセスが立ち上がる時
        index_mo = re.search(r'[p][r][o][c]\s\s[0-9]', line)
        mo_start = index_mo.start()
        proc = line[mo_start:mo_start+7]
        start_node_list += [proc]
        node_pos_list += [[rootnode_xpos, 0]]
        fw.write(str(node_id) + "[label = \"" + proc + "\",\n" )
        fw.write("pos = \"" + str(rootnode_xpos) + ",0!\"];\n")
        current_id_list += [node_id]
        node_id += 1
        rootnode_xpos += 2
        num_proc += 1
    else:
        index_mo = re.search(r'[p][r][o][c]\s\s[0-9]', line)
        if index_mo != None:
            mo_start = index_mo.start()
            proc_comp = line[mo_start:mo_start+7]
            # print(proc_comp)
            if proc_comp in start_node_list:
                snl_index = start_node_list.index(proc_comp)
                x = 0
                while x < num_proc:
                    node_pos_list[x][1] -= 1
                    x += 1
                node_label = node_id -2
                fw.write(str(node_id) + "[label = \"" + str(node_label) + "\",\n")
                fw.write("pos = \"" + str(node_pos_list[snl_index][0]) + "," + str(node_pos_list[snl_index][1]) + "!\"];\n")
                fw.write(str(current_id_list[snl_index]) + "->" + str(node_id) + ";\n")
                current_id_list[snl_index] = node_id
                node_id += 1
                seq_num += 1
        elif index_mo == None:
            break


    line = f.readline()

fw.write("}")
f.close()
fw.close()
print(start_node_list)
print(current_id_list)
print(node_pos_list)
print(num_proc)