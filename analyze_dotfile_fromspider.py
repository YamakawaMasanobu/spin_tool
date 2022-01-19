#SPINSPIDERから出力されたdotファイルから状態に関する情報を抽出

import re
state_info_list = [] #状態の情報を格納するlistのlist
edge_list=[]    #状態の接続関係を格納するstrのlist
state_dict = {}
sedge_list = []
pstate_dict = {}
cstate_dict = {}

# dotfilename = input("filename:")
dotfilename = "jikken.dot"
f = open(dotfilename, "r")
line = f.readline()
while(line):
    def_node_mo = re.match(r"[0-9]+\s*[[]", line)
    def_edge_mo = re.match(r"([0-9]+\s(->)\s[0-9]+)", line)
    if def_node_mo != None:
        state_info_mo = re.search("(\".*\")",line)
        state_info = state_info_mo.group().replace("\"", "")
        state_info_list.append(state_info.split("\\n"))
    elif def_edge_mo != None:
        edge_list.append(def_edge_mo.group())
    else:
        pass
    line = f.readline()

i = 0
temp_dict = {}
while(i < len(state_info_list)):
    j = 0
    while(j < len(state_info_list[i]) - 1):
        temp_dict[j] = state_info_list[i][j]
        j += 1
    state_dict[i] = temp_dict
    i += 1


i = 0
while(i < len(edge_list)):
    sedge_list = edge_list[i].split()
    #親ノードの辞書を作成
    if sedge_list[0] not in cstate_dict.keys():
        cstate_dict[sedge_list[0]] = [sedge_list[2]]
    else:
        if sedge_list[2] not in cstate_dict[sedge_list[0]]:
            cstate_dict[sedge_list[0]].append(sedge_list[2])
        else:
            pass
    #子ノードの辞書を作成    
    if sedge_list[2] not in pstate_dict.keys():
        pstate_dict[sedge_list[2]] = [sedge_list[0]]
    else:
        if sedge_list[0] not in pstate_dict[sedge_list[2]]:
            pstate_dict[sedge_list[2]].append(sedge_list[0])
        else:
            pass
    
    i += 1


# print(pstate_dict)
# print("\n\n")
# print(cstate_dict)
# print(state_dict)
# print(edge_list)
# print(state_info_list)

f.close()