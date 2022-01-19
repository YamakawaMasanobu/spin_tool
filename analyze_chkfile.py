import re
import analyze_dfile


end_flag = False
variable_list = []
num_list = []
chkstate_dict = {}

# filename = input("filename(chk):")
filename = "jikken.chk"

while not end_flag: 
    variable_list.append(input("variable(Enter in the same order as entered in jspin):"))
    judge = input("continue?(y/n)")
    if judge == "n":
        end_flag = True
    elif judge == "y":
        pass
    else:
        print("No")
        exit()        

f = open(filename, "r")
f_line = f.readline()

re_str = r"(\*spd\*)(\s)(.*)(" + re.escape(variable_list[0]) + r")(\s)(.*)"
while(f_line):
    newstate_mo = re.search(r"(\s*)(New state)(\s*)([0-9]+)", f_line)
    if newstate_mo != None:
        state_name = newstate_mo.group(4)
        f_line = f.readline()
        source_mo = re.search(re_str, f_line)
        numbers = source_mo.group(3)
        num_list = numbers.split()
        del num_list[0]
        del num_list[-1]

        i = 0
        lc_list = []
        while(i < len(num_list)):
            lc_list.append(analyze_dfile.proc_dict_forchk[i][num_list[i]])
            # print(analyze_dfile.proc_dict_forchk[i][num_list[i]])
            i += 1        
        chkstate_dict[state_name] = lc_list

    
    f_line = f.readline()
    
# print(chkstate_dict)
f.close()