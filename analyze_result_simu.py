#ランダムシミュレーションのログとSPINSPIDERのdotファイルから抽出された情報をてらしあわせる

import re
import analyze_dfile

f = open("result_simu.txt", "r")
f_line = f.readline()
line_num = 0

while(f_line):
    creates = f_line.find("creates")
    proc_log_mo = re.match(r"\s*[0-9]+:\s+proc", f_line)
    breakpoint_mo = re.match(r"#process", f_line)
    if proc_log_mo != None and creates == -1:
        tmp_list =f_line.split()
        # print(tmp_list)
        proc_name_mo = re.search(r"(\()(.*)(:)(.*)", tmp_list[3])
        proc_name = proc_name_mo.group(2)
        line_mo = re.search(r"(.*)(\.pml:)([0-9]+)", tmp_list[4])
        line_num = line_mo.group(3)
        proc_key = analyze_dfile.proc_dict[proc_name].keys()
        # print(proc_key)
        if line_num in proc_key:
            new_line = f_line.replace(tmp_list[7], analyze_dfile.proc_dict[proc_name][line_num])
            print(new_line) 
            # print(line_num)
        else:
            new_line.replace(f_line, "")
            print(new_line)
            # print(line_num)
    elif breakpoint_mo != None:
        break
    else:
        pass

    f_line = f.readline()
f.close()