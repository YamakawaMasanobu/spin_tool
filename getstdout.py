import subprocess, sys

filename = input("file name: ")

cp = subprocess.run(['spin', '-p', filename], encoding='utf-8', stdout=subprocess.PIPE)
print(f'*** file names: \n{cp.stdout}'
      f'*** total {len(cp.stdout.splitlines())} files')
with open('result_simu.txt', 'w') as fp:
    cp = subprocess.run(['spin', '-p', filename], stdout=fp)

args = ["python3", "toolish.py"]
try:
    res = subprocess.check_output(args)
except:
    print("Error")