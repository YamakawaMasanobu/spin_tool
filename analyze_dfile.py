import re
import collections

location_counter = ""
line_num = 0
state_num = 0
process_name = ""
proc_dict = {}

f = open("dfile.txt", "r")
line = f.readline()

while(line):
    proc_mo = re.match(r"(proctype)", line)
    state_mo = re.match(r"\s*(state)\s*[0-9]+", line)

    if proc_mo != None:
        Match_Object = re.match(r"(proctype)\s+(.*)", line)
        process_name = Match_Object.group(2)
        proc_dict[process_name] = {}
    elif state_mo != None:
        l_lc_mo = re.search(r"(.pml:)([0-9]+)\s(=>)\s(.*)", line) #ロケーションカウンターとその行番号を抽出
        proc_dict[process_name][l_lc_mo.group(2)] = l_lc_mo.group(4)
    else:
        pass
    line = f.readline()

print(proc_dict)
f.close()