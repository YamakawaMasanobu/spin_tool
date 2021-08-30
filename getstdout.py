import subprocess, sys

cp = subprocess.run(['spin', '-p', 'Katsupay_spin.pml'], encoding='utf-8', stdout=subprocess.PIPE)
print(f'*** file names: \n{cp.stdout}'
      f'*** total {len(cp.stdout.splitlines())} files')
with open('result_simu.txt', 'w') as fp:
    cp = subprocess.run(['spin', '-p', 'Katsupay_spin.pml'], stdout=fp)

args = ["python3", "toolish.py"]
try:
    res = subprocess.check_output(args)
except:
    print("Error")