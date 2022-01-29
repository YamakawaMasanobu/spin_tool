import re
from collections import defaultdict

process_name = ""
proc_dict_forers = {}
proc_dict_forchk= {}
proc_num = -1

f = open("dfile.txt", "r")
line = f.readline()

while(line):
    proc_mo = re.match(r"(proctype)", line)
    state_mo = re.match(r"\s*(state)\s*[0-9]+", line)

    if proc_mo != None:
        proc_num += 1
        Match_Object = re.match(r"(proctype)\s+(.*)", line)
        process_name = Match_Object.group(2)
        proc_dict_forchk[proc_num] = {}
        proc_dict_forers[process_name] = {}
    elif state_mo != None:
        source_mo = re.search(r"(\s*)(state)(\s+)([0-9][0-9]*)(\s-\(tr)(.*)", line) #source state
        l_lc_mo = re.search(r"(.pml:)([0-9][0-9]*)\s(=>)\s(.*)", line) #ロケーションカウンターとその行番号を抽出
        if source_mo.group(4) not in proc_dict_forchk[proc_num]:
            proc_dict_forchk[proc_num][source_mo.group(4)] = []
        else:
            pass
            
        if l_lc_mo.group(2) + "." + l_lc_mo.group(4) not in proc_dict_forchk[proc_num][source_mo.group(4)]:
            proc_dict_forchk[proc_num][source_mo.group(4)].append(l_lc_mo.group(2) + "." + l_lc_mo.group(4))
        else:
            pass
        
        if l_lc_mo.group(2) not in proc_dict_forers[process_name]:
            proc_dict_forers[process_name][l_lc_mo.group(2)] = []
        else:
            pass
                        
        if l_lc_mo.group(4) not in proc_dict_forers[process_name][l_lc_mo.group(2)]:
            proc_dict_forers[process_name][l_lc_mo.group(2)].append(l_lc_mo.group(4))
        else:
            pass
        
    else:
        pass
    line = f.readline()

# print(proc_dict_forchk)
# print("\n\n")
# print(proc_dict_forers)
f.close()