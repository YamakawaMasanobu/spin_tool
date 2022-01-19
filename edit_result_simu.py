#ランダムシミュレーションのログをdファイルをもとに編集
#メッセージの書き換えと不要な行の削除

import re
import analyze_dfile

f = open("result_simu.txt", "r")
fw = open ("edited_result_simu.txt", "w")
f_line = f.readline()
line_num = 0

while(f_line):
    creates = f_line.find("creates")
    proc_log_mo = re.match(r"\s*[0-9]+:\s+proc", f_line)
    breakpoint_mo = re.match(r"#process", f_line)
    if creates != -1:
        fw.write(f_line)
    elif proc_log_mo != None and creates == -1:
        proc_name_mo = re.search(r"(\()(.*)(:)([0-9]+)(\))", f_line)
        proc_name = proc_name_mo.group(2)
        line_mo = re.search(r"(\.pml:)([0-9]+)", f_line)
        line_num = line_mo.group(2)
        proc_key = analyze_dfile.proc_dict_forers[proc_name].keys()
        if line_num in proc_key:
            lc_mo = re.search(r"\[(.*)\]", f_line)
            location_counter = lc_mo.group()
            if len(analyze_dfile.proc_dict_forers[proc_name][line_num]) == 1:
                new_line = f_line.replace(location_counter, analyze_dfile.proc_dict_forers[proc_name][line_num][0])
            else:
                i = 0
                while i < len(analyze_dfile.proc_dict_forers[proc_name][line_num]):
                    if lc_mo.group(1) == analyze_dfile.proc_dict_forers[proc_name][line_num][i]:
                        new_line = f_line.replace(location_counter, analyze_dfile.proc_dict_forers[proc_name][line_num][i])
                    else:
                        pass
                    i += 1
            fw.write(new_line)
        else:
            pass
    elif breakpoint_mo != None:
        break
    else:
        pass

    f_line = f.readline()
f.close()
fw.close()