from os import truncate
import re
import analyze_chkfile
import analyze_dotfile_fromspider

current_lc_dict = {}

re_str = r"(.*)(proc\s\s)([0-9]+)(.*)(.pml:)([0-9]+)(\s\(state\s[0-9]+\)\s)(.*)"


def set_start_state(current_lc_dict):  #初期状態のセット
    searched_num_list = []
    f = open("edited_result_simu.txt", "r")
    line = f.readline()
    while(line):
        root = line.find("root")
        if root == -1:
            lc_mo = re.search(re_str, line)
            if lc_mo != None and lc_mo.group(3) not in searched_num_list:
                current_lc_dict[lc_mo.group(3)] = lc_mo.group(6) + ". " + lc_mo.group(8)
                searched_num_list.append(lc_mo.group(3))
            else:
                pass
        else:
            pass
        
        line = f.readline()
    f.close()
    
def check_inchk(lc, proc_num): #lcがchkファイルをもとに作成した状態の辞書の指定したプロセスの中にあるか判定
    i = 0
    state_list = []
    while i < len(analyze_chkfile.chkstate_dict):
        j = 0
        while j < len(analyze_chkfile.chkstate_dict[str(i)][int(proc_num)]):
            if lc in analyze_chkfile.chkstate_dict[str(i)][int(proc_num)][j]:
                state_list.append(i)
                j += 1
            else:
                j += 1
        i += 1
    if len(state_list) == 0:
        return [0]
    else:
        return [1, state_list]
    

f = open("edited_result_simu.txt", "r")
f_line = f.readline()

set_start_state(current_lc_dict)


while(f_line):
    root = f_line.find("root")
    if root == -1:
        lc_mo = re.search(re_str, f_line)
        lc = lc_mo.group(6) + ". " + lc_mo.group(8)
        current_lc_dict[lc_mo.group(3)] = lc
        i = 0
        #ロケーションカウンターが全て合致する状態の探索
        while i < len(current_lc_dict):
            a = check_inchk(current_lc_dict[str(i)], i)
            if a[0] != 0:
                if i == 0:
                    tmp = a[1]
                else:
                    tmp = set(tmp) & set(a[1])
                    tmp_list = list(tmp)
            i += 1

        print(tmp_list)    
                
                
        # print(current_lc_dict)
        
        # in_chk = check_inchk(lc, lc_mo.group(3))
        # if in_chk[0] == 1:
            # print(in_chk[1])
        
    
    
    f_line = f.readline()

f.close()