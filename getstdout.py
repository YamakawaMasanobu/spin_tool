import subprocess, sys

filename = input("file name: ")

cp = subprocess.run(['spin', '-p', filename], encoding='utf-8', stdout=subprocess.PIPE)
print(f'*** file names: \n{cp.stdout}'
      f'*** total {len(cp.stdout.splitlines())} files')
with open('result_simu.txt', 'w') as fp:
    cp = subprocess.run(['spin', '-p', filename], stdout=fp)

cp = subprocess.run(['spin', '-a', filename], encoding='utf-8', stdout=subprocess.PIPE)
cp = subprocess.run(['gcc', '-o', 'pan', 'pan.c'], encoding = 'utf-8', stdout=subprocess.PIPE)
cp = subprocess.run(['./pan', '-d'], encoding='utf-8', stdout=subprocess.PIPE)
print(f'*** file names: \n{cp.stdout}'
      f'*** total {len(cp.stdout.splitlines())} files')
with open('dfile.txt', 'w') as fp:
    cp = subprocess.run(['./pan', '-d'], stdout=fp)

args = ["python3", "UMLgenerater.py"]
try:
    res = subprocess.check_output(args)
except:
    print("Error")


