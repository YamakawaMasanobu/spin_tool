import re

filename = input("filename(dot):")
# filename = "jikken.dot"
tmp = filename.replace(".dot", "")

state_list = []
state_dict = {}
state_name =""
root_node = ""
child_node = ""
edge_list = []
root_node_dict = {}
child_node_dict = {}
defined_state_list = []

f = open(filename, "r")
fw = open (tmp + ".pu", "w")
fw.write("@startuml statemachine\n")

def writestate(state, state_dict):
    fw.write("state state" + state + "{\n")
    fw.write("state state" + state + ":" + state_dict[state] + "\n}\n")
    defined_state_list.append(state)

def check_state_in1out1(root_node_dict, child_node_dict, state):
    if root_node_dict[state] == 1 and child_node_dict[state] ==1:
        return 1
    else:
        return -1

def check_child_node(edge_list, root_node_dict, child_node_dict, state, state_dict):
    for edge in edge_list:
        sedge_list = edge.split()
        if state == sedge_list[0]:
            a = check_state_in1out1(root_node_dict, child_node_dict, sedge_list[2])
            if a == 1:
                writestate(sedge_list[2], state_dict)
                check_child_node(edge_list, root_node_dict, child_node_dict, sedge_list[2], state_dict)
            elif a == -1:
                fw.write("}\n")
        else:
            pass
                
f_line = f.readline()
while(f_line):
    def_node_mo = re.match(r"([0-9]+)\s*(\[)", f_line)
    def_edge_mo = re.match(r"(([0-9]+)\s(->)\s([0-9]+))", f_line)
    if def_node_mo != None:
        state_name = def_node_mo.group(1)
        state_list.append(state_name)
        root_node_dict[state_name] = 0
        child_node_dict[state_name] = 0
        state_label_mo = re.search("(\".*\")",f_line)
        state_label = state_label_mo.group().replace("\"", "")
        state_dict[state_name] = state_label
    elif def_edge_mo != None:
        edge_list.append(def_edge_mo.group())
        root_node = def_edge_mo.group(2)
        child_node = def_edge_mo.group(4)
        root_node_dict[root_node] += 1
        child_node_dict[child_node] += 1
    else:
        pass
    f_line = f.readline()

i = 1
for current_state in state_list:
    if current_state not in defined_state_list:
        if check_state_in1out1(root_node_dict, child_node_dict, current_state) == 1:
            for edge in edge_list:
                sedge_list = edge.split()
                if current_state == sedge_list[0]:
                    if check_state_in1out1(root_node_dict, child_node_dict, sedge_list[2]) == 1:
                        fw.write("state statebrock_" + str(i) + "{\n")
                        i += 1
                        writestate(current_state, state_dict)
                        writestate(sedge_list[2], state_dict)

                        check_child_node(edge_list, root_node_dict, child_node_dict, sedge_list[2], state_dict)
                    else:
                        writestate(current_state, state_dict)
        else:
            writestate(current_state, state_dict)
    else:
        pass 

for edge in edge_list:
    sedge_list = edge.split()
    fw.write("state" +sedge_list[0] + " --> state" + sedge_list[2] + "\n")     
            

# print(state_dict)
# print(root_node_dict)
# print("\n")
# print(child_node_dict)
fw.write("@enduml")
f.close()
fw.close()