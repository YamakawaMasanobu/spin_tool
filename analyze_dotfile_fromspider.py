#SPINSPIDERから出力されたdotファイルから状態に関する情報を抽出

import re
import collections
state_info_list = [] #状態の情報を格納するlistのlist
edge_list=[]    #状態の接続関係を格納するstrのlist

dotfilename = input("filename:")
# dotfilename = "jikken.dot"
f = open(dotfilename, "r")
line = f.readline()
while(line):
    def_node_mo = re.match(r"[0-9]+\s*[[]", line)
    def_edge_mo = re.match(r"([0-9]+\s(->)\s[0-9]+)", line)
    if def_node_mo != None:
        state_info_mo = re.search("(\".*\")",line)
        state_info = state_info_mo.group().replace("\"", "")
        state_info_list.append( state_info.split("\\n"))
    elif def_edge_mo != None:
        edge_list.append(def_edge_mo.group())
    else:
        pass
    line = f.readline()

print(state_info_list)
print(edge_list)

f.close()