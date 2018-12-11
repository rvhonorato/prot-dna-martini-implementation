# create the izone based on structural alignment
import subprocess
import glob
from itertools import groupby
from operator import itemgetter


def split_chain(pdbf):
    pdb_name = pdbf.split('.pdb')[0]
    cmd = 'python /home/rodrigo/pdb-tools/pdb_splitchain.py {}'.format(pdbf)
    subprocess.Popen(cmd.split())
    pdb_dic = {k.split('_')[-1].split('.pdb')[0]: k for k in glob.glob('{}_*'.format(pdb_name))}
    return pdb_dic


def align(prota, protb):
    pad = split_chain(prota)
    pbd = split_chain(protb)

    # check if chain ids match
    if pad.keys() != pbd.keys():
        print('ChainIDs do not match!')
        exit()

    numbering_dic = {}
    for chain in pad.keys():
        numbering_dic[chain] = {}
        cmd = '{} -p1 {} -p2 {} -c1 {} -c2 {}'.format(lovoalign_exe, pad[chain], pbd[chain], chain, chain)
        out = subprocess.getoutput(cmd).split('\n')

        aln_start = 27  # careful with this
        aln_end = [i - 2 for i, k in enumerate(out[aln_start:]) if 'FINAL' in k][0] + aln_start
        aln_l = out[aln_start:aln_end]

        aln = [aln_l[i:i + 3][:2] for i in range(0, len(aln_l), 3)]

        for e in aln:
            a, b = e

            a = a.split()
            b = b.split()

            a_seq = a[1]
            b_seq = b[1]

            a_count = int(a[0])
            b_count = int(b[0])

            for a_aa, b_aa in zip(a_seq, b_seq):
                if a_aa != '-' and b_aa != '-':
                    numbering_dic[chain][a_count] = b_count

                if a_aa != '-':
                    a_count += 1

                if b_aa != '-':
                    b_count += 1

    return numbering_dic

def identify_inteface(pdbf, cutoff):

    cmd = '{} {} {}'.format(contacts_exe, pdbf, cutoff)
    contacts_l = subprocess.getoutput(cmd).split('\n')

    interface_dic = {}
    for l in contacts_l:
        resnumA, chainA, atomA, resnumB, chainB, atomB, distance = l.split()
        resnumA = int(resnumA)
        resnumB = int(resnumB)

        # One way
        try:
            _ = interface_dic[chainA]
        except:
            interface_dic[chainA] = {}
        try:
            _ = interface_dic[chainA][chainB]
        except:
            interface_dic[chainA][chainB] = []

        if float(distance) <= cutoff:
            if resnumA not in interface_dic[chainA][chainB]:
                interface_dic[chainA][chainB].append(resnumA)

        # other way
        try:
            _ = interface_dic[chainB]
        except:
            interface_dic[chainB] = {}
        try:
            _ = interface_dic[chainB][chainA]
        except:
            interface_dic[chainB][chainA] = []

        if float(distance) <= cutoff:
            if resnumB not in interface_dic[chainB][chainA]:
                interface_dic[chainB][chainA].append(resnumB)

    return interface_dic

def get_range(data):
    ranges =[]
    for k,g in groupby(enumerate(data),lambda x:x[0]-x[1]):
        group = (map(itemgetter(1),g))
        group = list(map(int,group))
        ranges.append((group[0],group[-1]))
    return ranges

def retrieve_izone(c_dic, numbering_dic):
    # based on the reference interface, create izone
    izone_l = []
    for chain in c_dic:
        ref_dic = {}
        for bound_res in list(c_dic[chain].items())[0][1]:
            try:
                ub = numbering_dic[chain][bound_res]
                ref_dic[bound_res] = ub
            except:
                pass

        # define the bound ranges ex (1-20)
        for bound_range in get_range(ref_dic.keys()):
            #  check which is the unbound range that matches
            unbound_res_l = []
            for bound_res in range(bound_range[0], bound_range[1]+1):
                # unbound_res = ref_dic[bound_res]
                unbound_res_l.append(ref_dic[bound_res])

            # use unbound_res_l to build zones
            for unbound_range in get_range(unbound_res_l):
                bound_res_l = []
                for unbound_res in range(unbound_range[0],unbound_range[1]+1):
                    # find what it the bound res that correspond to this unbound
                    # bound_res_l.append(find_key(ref_dic, unbound_res))
                    bound_res_l.append(list(ref_dic.keys())[list(ref_dic.values()).index(unbound_res)])
                #
                rangeA = get_range(bound_res_l)[0] # bound
                rangeB = unbound_range
                #
                # print chain, rangeA, rangeB
                #
                izone_str = 'ZONE %s%i-%s%i:%s%i-%s%i' % (chain, rangeA[0], chain, rangeA[1], chain, rangeB[0], chain, rangeB[1])
                izone_l.append(izone_str)

    return izone_l

lovoalign_exe = '~/software/lovoalign-18.320/bin/lovoalign'
contacts_exe = '~/haddock-CSB-tools/contact-anal/contact'

def run_profit(prot_a, prot_b, atoms, izone_l):
    cmd = 'refe %s\nmobi %s\nATOMS %s\nZONE CLEAR\n%s\nstatus\nFIT\nquit' % (prot_a, prot_b, atoms, '\n'.join(izone_l))
    # run!
    open('irmsd.dbg', 'w').write(cmd)
    out = subprocess.getoutput('echo "%s" | /home/rodrigo/software/ProFitV3.1/src/profit' % cmd).split('\n')


def main():
    pa = 'ref.pdb'
    pb = 'irmsd-test2/structures/it1/water/complex_1w.pdb'

    num_dic = align(pa, pb)
    contact_dic = identify_inteface(pa, 5.0)

    izone_list = retrieve_izone(contact_dic, num_dic)
    # TODO: Parse result
    run_profit(pa, pb, 'CA', izone_list)


if __name__ == '__main__':
    main()