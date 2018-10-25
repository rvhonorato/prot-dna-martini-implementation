# find what is different between two run.cns files
import sys
import re

p_regex = r"{===>}\s(.*)="
v_regex = r"{===>}\s.*=(.*);"

param_dic = {}
param_ignore = ['pcs', 'rdc', 'his', 'krg', 'prot', 'dir', 'cns', 'cpunumber']

for l in open(sys.argv[1]):
    if '{===>}' in l:
        param = re.findall(p_regex, l)[0]
        try:
            _ = param_dic[param]
        except:
            param_dic[param] = {1: None, 2: None}

for l in open(sys.argv[2]):
    if '{===>}' in l:
        param = re.findall(p_regex, l)[0]
        try:
            _ = param_dic[param]
        except:
            param_dic[param] = {1: None, 2: None}

for l in open(sys.argv[1]):
    if '{===>}' in l:
        param = re.findall(p_regex, l)[0]
        value = re.findall(v_regex, l)[0]
        param_dic[param][1] = value

for l in open(sys.argv[2]):
    if '{===>}' in l:
        param = re.findall(p_regex, l)[0]
        value = re.findall(v_regex, l)[0]
        param_dic[param][2] = value

print 'param\t%s\t%s' % (sys.argv[1], sys.argv[2])
for p in param_dic:
    v1 = param_dic[p][1]
    v2 = param_dic[p][2]
    #
    if v1 != v2:
        if v1 and v2:
            if not [e for e in param_ignore if e in p]:
                print '%s\t%s\t%s' % (p, v1, v2)