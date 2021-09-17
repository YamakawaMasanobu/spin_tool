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
current_step = 0

fw = open("sequence.dot", "w")
f = open("result_simu.txt", "r")

fw.write("digraph sequence{\n")

line = f.readline()

while(line):    #ログを一行ずつ解析
    start = line.find("Starting")
    root = line.find("root")

    
    if start != -1:     #プロセスを開始させる時
        step_num = re.match(r"\s*[0-9]+", line)
        index = line.find("pid")
        pid = line[index:]
        start_node_list += pid
        current_id_list += node_id
        current_step = step_num.group()
        node_id += 1
    elif root != -1:        #アクティブなプロセスが立ち上がる時
        step_num = re.match(r"\s*[0-9]+", line)
        index_mo = re.search(r'[p][r][o][c]\s+[0-9]', line)  #match object
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
        current_step = step_num.group()
    else:
        step_num = re.match(r"\s*[0-9]+", line)
        index_mo = re.search(r'[p][r][o][c]\s+[0-9]', line)
        if index_mo != None:
            mo_start = index_mo.start()
            proc_comp = line[mo_start:mo_start+7]
            if proc_comp in start_node_list:
                snl_index = start_node_list.index(proc_comp)
                if current_step != step_num.group():
                    x = 0
                    while x < num_proc:
                        node_pos_list[x][1] -= 1
                        x += 1
                else:
                    pass
                # node_label = node_id -2
                fw.write(str(node_id) + "[label = \"" + str(step_num.group()) + "\",\n")
                fw.write("pos = \"" + str(node_pos_list[snl_index][0]) + "," + str(node_pos_list[snl_index][1]) + "!\"];\n")
                fw.write(str(current_id_list[snl_index]) + "->" + str(node_id) + ";\n")
                current_id_list[snl_index] = node_id
                node_id += 1
                seq_num += 1
                current_step = step_num.group()
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