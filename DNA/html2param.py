# convert new.html to new.param
import glob
import os

folder_list = [f for f in glob.glob('/home/rodrigo/dna-benchmark/*') if not '.' in f]

for folder in folder_list:
    html_f = f'{folder}/new.html'
    param_f = f'{folder}/run.param'
    param_out = open(param_f, 'w')
    print(param_f)
    for l in open(html_f).readlines():
        new_l = None
        if not l.startswith('<') and not 'submit_save' in l:
            new_l = l.split('<')[0]
        if 'HADDOCK_DIR' in l:
            new_l = f'HADDOCK_DIR={os.environ["HADDOCK"]}'
        if 'RUN_NUMBER' in l:
            new_l = 'RUN_NUMBER=1'
        if new_l:
            param_out.write(f'{new_l}\n')
    param_out.close()
