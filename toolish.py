from platform import node
from graphviz import Graph
from graphviz import Digraph
import re
import collections

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
current_state_list= []
state_list = [] 
state_link_list = []
state_message_list = []
childnode_list = []
parentnode_list = [] 

fw = open("sequence.dot", "w")
f = open("result_simu.txt", "r")
fw.write("digraph sequence{\n")

line = f.readline()

def write_statemachine(state_list, parentnode_list, childnode_list, state_link_list, num_proc, state_message_list):
    sm = open("statemachine.pu", "w")
    sm.write("@startuml statemachine\n\n")
    state_in_list = count_in(parentnode_list, num_proc)
    state_out_list = count_out(childnode_list, num_proc)
    inout_1_state_list = extract_inout_1_state(state_in_list, state_out_list, num_proc)
    searched_state_list = []
    defined_state_list = []
    num_baseblock = 1

    i = 0
    while i < num_proc:
        j = 0
        while j < len(state_list[i]):
            if state_list[i][j] not in searched_state_list:
                # print(state_list[i][j])
                # print(searched_state_list)
                # print("\n")
                if state_list[i][j] not in inout_1_state_list[i]:
                    msg_index = extract_index(state_message_list[i], state_list[i][j])
                    sm.write("state " + state_list[i][j] + "{\nstate " + state_message_list[i][msg_index] + "}\n")
                    searched_state_list.append(state_list[i][j])
                else:
                    next_state = extract_after_arrow(parentnode_list[i], state_list[i][j], state_link_list[i])
                    if next_state not in inout_1_state_list[i]:
                        msg_index = extract_index(state_message_list[i], state_list[i][j])
                        sm.write("state " + state_list[i][j] + "{\nstate " + state_message_list[i][msg_index] + "}\n")
                        searched_state_list.append(state_list[i][j])
                    else:
                        sm.write("state state" + str(num_baseblock) + "{\n")
                        msg_index = extract_index(state_message_list[i], state_list[i][j])
                        sm.write("state " + state_list[i][j] + "{\nstate " + state_message_list[i][msg_index] + "}\n")
                        searched_state_list.append(state_list[i][j])
                        msg_index = extract_index(state_message_list[i], next_state)
                        sm.write("state " + next_state + "{\nstate " + state_message_list[i][msg_index] + "}\n")
                        searched_state_list.append(next_state)
                        while extract_after_arrow(parentnode_list[i], next_state, state_link_list[i]) in inout_1_state_list[i]:
                            atn_state = extract_after_arrow(parentnode_list[i], next_state, state_link_list[i])
                            msg_index = extract_index(state_message_list[i], atn_state)
                            sm.write("state " + atn_state + "{\nstate " + state_message_list[i][msg_index] + "}\n")
                            searched_state_list.append(atn_state)
                            next_state = atn_state
                        else:
                            atn_state = extract_after_arrow(parentnode_list[i], next_state, state_link_list[i])
                            sm.write("}\n")
                            num_baseblock += 1
                            if atn_state not in searched_state_list:
                                msg_index = extract_index(state_message_list[i], atn_state)
                                sm.write("state " + atn_state + "{\nstate " + state_message_list[i][msg_index] + "}\n")
                                searched_state_list.append(atn_state)
            else:
                pass
            j += 1
        i += 1

    i = 0
    while i < num_proc:
        j = 0
        while j < len(state_link_list[i]):
            sm.write("\n" + state_link_list[i][j] + "\n")
            j +=1
        i += 1
    

    sm.write("@enduml")
    sm.close

def extract_index(list, target):
    for i, e in enumerate(list):
        if target in e:
            return i
        # raise IndexError
    
def extract_after_arrow(parentnode_list, state_name, link_list):
    target = "-->"
    index = parentnode_list.index(state_name)
    a = link_list[index].find(target)
    r = link_list[index][a + len(target):]
    return r

def extract_inout_1_state(state_in_list, state_out_list, num_proc):
    inout_1_state_list = []
    i = 0
    while i < num_proc:
        j = 0
        temp_list = []
        while j < len(state_list[i]):
            if state_in_list[i][state_list[i][j]] == 1 and state_out_list[i][state_list[i][j]] == 1:
                temp_list.append(state_list[i][j])
            j += 1
        inout_1_state_list.append(temp_list)
        i += 1
    return inout_1_state_list

def count_in(parentnode_list, num_proc):
    i = 0
    state_in_list = []
    while i < num_proc:
        state_in_list += [collections.Counter(parentnode_list[i])]
        i += 1
    return state_in_list

def count_out(childnode_list, num_proc):
    i = 0
    state_out_list = []
    while i < num_proc:
        state_out_list += [collections.Counter(childnode_list[i])]
        i += 1
    return state_out_list





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
        childnode_list += [[]]
        current_state_list += ["[*]"]
        parentnode_list += [[]]
        state_link_list += [[]]
        state_message_list += [[]]
        state_list += [[]]
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
        state_mo = re.search(r'[s][t][a][t][e]\s[0-9]+', line)
        if index_mo != None:
            #以下シーケンス図に関する記述
            mo_start = index_mo.start()
            mo_end = index_mo.end()
            proc_comp = line[mo_start:mo_end]
            if proc_comp in start_node_list:
                snl_index = start_node_list.index(proc_comp)
                if current_step != step_num.group():
                    x = 0
                    while x < num_proc:
                        node_pos_list[x][1] -= 1
                        x += 1
                else:
                    pass
                fw.write(str(node_id) + "[label = \"" + str(step_num.group()) + "\",\n")
                fw.write("pos = \"" + str(node_pos_list[snl_index][0]) + "," + str(node_pos_list[snl_index][1]) + "!\"];\n")
                fw.write(str(current_id_list[snl_index]) + "->" + str(node_id) + "\n")
                edge_label_mo = re.search(r"[\[].*[\]]",line)
                edge_label = edge_label_mo.group()
                fw.write("[label = \"" + edge_label + "\"]\n")
                current_id_list[snl_index] = node_id
                node_id += 1
                seq_num += 1
                current_step = step_num.group()

            #以下状態線図に関する記述    
            smo_start = state_mo.start()  #状態遷移をリスト化
            smo_end = state_mo.end()
            state = line[smo_start:smo_end] + "_" + str(snl_index)
            nonspace_state = state.replace(" ", "")
            if nonspace_state not in state_list[snl_index]:
                state_list[snl_index].append(nonspace_state)
            state_link = current_state_list[snl_index] + "-->" + nonspace_state
            if state_link not in state_link_list[snl_index]:
                # sm.write(state_link + "\n")
                # sm.write(nonspace_state + ":" + edge_label + "\n")
                state_message = nonspace_state + ":" + edge_label + "\n"
                state_link_list[snl_index] += [state_link]
                state_message_list[snl_index] += [state_message]
                childnode_list[snl_index] += [nonspace_state]
                parentnode_list[snl_index] += [current_state_list[snl_index]]
            else:
                pass
            current_state_list[snl_index] = nonspace_state
            
            
        elif index_mo == None:
            break


    line = f.readline()
write_statemachine(state_list, parentnode_list, childnode_list, state_link_list, num_proc, state_message_list)


fw.write("}")
f.close()
fw.close()


# print(start_node_list)
# print(current_id_list)
# print(node_pos_list)
# print("\n\n\n")
# print(state_list)
# print(state_link_list)
# print("\n\n\n")
# print(state_message_list)
# print(num_proc)
# print("\n\n\n")
# print(childnode_list)
# print("\n\n\n")
# print(parentnode_list)