# create the izone based on structural alignment
import argparse
import shutil
import subprocess
import glob
import os
from itertools import groupby
from operator import itemgetter


def split_chain(pdbf):
    # """ inpsired """ by https://github.com/JoaoRodrigues/pdb-tools ;)

    prev_chain, chain_ids, chain_atoms = None, [], {}
    cur_chain = None
    for line in open(pdbf):
        if 'ATOM' in line[:4]:
            if prev_chain != line[21]:
                if not line[21] in chain_atoms:
                    cur_chain = chain_atoms[line[21]] = []
                else:
                    cur_chain = chain_atoms[line[21]]
                cur_chain.append(line)
                prev_chain = line[21]
                chain_ids.append(line[21])
            else:
                cur_chain.append(line)

    # Output chains to files
    pdb_dic = {}
    for c_id in chain_ids:
        name = pdbf.split('.pdb')[0] + '_' + c_id + '.pdb'
        pdb_dic[c_id] = name
        out = open(name, 'w')
        out.write(''.join(chain_atoms[c_id]))
        out.write('END\n')
        out.close()

    return pdb_dic


def load_seq(prot):
    aa_dic = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLU': 'E',
              'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W',
              'TYR': 'Y', 'VAL': 'V'}
    seq_dic = {}
    for l in open(prot):
        if 'ATOM' in l[:4]:
            chain = l[21]
            resnum = int(l[22:26])
            resname = l[17:20]
            try:
                _ = seq_dic[chain]
            except KeyError:
                seq_dic[chain] = {}

            seq_dic[chain][resnum] = aa_dic[resname]
    return seq_dic


def align(prota, protb):
    pad = split_chain(prota)
    pbd = split_chain(protb)

    # check if chain ids match
    if pad.keys() != pbd.keys():
        print('ChainIDs do not match!')
        exit()

    # make sure of numbering
    pa_seqdic = load_seq(prota)
    pb_seqdic = load_seq(protb)

    numbering_dic = {}
    for chain in pad.keys():
        numbering_dic[chain] = {}
        cmd = 'lovoalign -p1 {} -p2 {} -c1 {} -c2 {}'.format(pad[chain], pbd[chain], chain, chain)
        out = subprocess.getoutput(cmd).split('\n')

        aln_start = [out.index(e) for e in out if 'SEQUENCE ALIGNMENT' in e][0] + 2
        aln_end = [i - 2 for i, k in enumerate(out[aln_start:]) if 'FINAL' in k][0] + aln_start
        aln_l = out[aln_start:aln_end]

        aln = [aln_l[i:i + 3][:2] for i in range(0, len(aln_l), 3)]

        for e in aln:
            a, b = e

            a = a.split()
            b = b.split()

            a_seq = a[1]
            b_seq = b[1]

            reslist_a = list(pa_seqdic[chain].keys())
            reslist_b = list(pb_seqdic[chain].keys())

            idx_a = 0
            idx_b = 0

            res_a = None
            res_b = None

            for a_aa, b_aa in zip(a_seq, b_seq):
                if a_aa != '-':
                    res_a = reslist_a[idx_a]
                    idx_a += 1

                if b_aa != '-':
                    res_b = reslist_b[idx_b]
                    idx_b += 1

                if a_aa != '-' and b_aa != '-':
                    numbering_dic[chain][res_a] = res_b

    return numbering_dic


def run_contacts(pdbf, cutoff):
    cmd = 'contact {} {}'.format(pdbf, cutoff)
    out = subprocess.getoutput(cmd).split('\n')
    return out


def identify_inteface(pdbf, cutoff):
    contacts_l = run_contacts(pdbf, cutoff)

    interface_dic = {}
    for l in contacts_l:
        resnum_a, chain_a, atom_a, resnum_b, chain_b, atom_b, distance = l.split()
        resnum_a = int(resnum_a)
        resnum_b = int(resnum_b)

        # One way
        try:
            _ = interface_dic[chain_a]
        except KeyError:
            interface_dic[chain_a] = {}
        try:
            _ = interface_dic[chain_a][chain_b]
        except KeyError:
            interface_dic[chain_a][chain_b] = []

        if float(distance) <= cutoff:
            if resnum_a not in interface_dic[chain_a][chain_b]:
                interface_dic[chain_a][chain_b].append(resnum_a)

        # other way
        try:
            _ = interface_dic[chain_b]
        except KeyError:
            interface_dic[chain_b] = {}
        try:
            _ = interface_dic[chain_b][chain_a]
        except KeyError:
            interface_dic[chain_b][chain_a] = []

        if float(distance) <= cutoff:
            if resnum_b not in interface_dic[chain_b][chain_a]:
                interface_dic[chain_b][chain_a].append(resnum_b)

    return interface_dic


def get_range(data):
    ranges = []
    for k, g in groupby(enumerate(data), lambda x: x[0] - x[1]):
        group = (map(itemgetter(1), g))
        group = list(map(int, group))
        ranges.append((group[0], group[-1]))
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
            except KeyError:
                pass

        for bound_range in get_range(ref_dic.keys()):
            unbound_res_l = []
            for bound_res in range(bound_range[0], bound_range[1] + 1):
                unbound_res_l.append(ref_dic[bound_res])

            for unbound_range in get_range(unbound_res_l):
                bound_res_l = []
                for unbound_res in range(unbound_range[0], unbound_range[1] + 1):
                    bound_res_l.append(list(ref_dic.keys())[list(ref_dic.values()).index(unbound_res)])

                range_a = get_range(bound_res_l)[0]  # bound
                range_b = unbound_range

                izone_str = 'ZONE %s%i-%s%i:%s%i-%s%i' % (
                    chain, range_a[0], chain, range_a[1], chain, range_b[0], chain, range_b[1])
                izone_l.append(izone_str)

    return izone_l


def run_profit(cmd):
    return subprocess.getoutput('echo "{}" | profit'.format(cmd)).split('\n')


def calc_irmsd(prot_a, prot_b, atoms, izone_l):
    irmsd = None

    cmd = 'refe %s\nmobi %s\nATOMS %s\nZONE CLEAR\n%s\nstatus\nFIT\nquit' % (prot_a, prot_b, atoms, '\n'.join(izone_l))
    open('irmsd.dbg', 'w').write(cmd)

    out = run_profit(cmd)

    try:
        irmsd = float(out[-1].split()[-1])
    except KeyError:
        print('Something went wrong when running PROFIT, check irmsd.dbg')
        exit()

    return irmsd


def calc_fnat(pa, pb, numbering_dic, cutoff=5.0):
    con_a = run_contacts(pa, cutoff)
    con_b = run_contacts(pb, cutoff)

    # match reference to target
    a_con_l = []
    for e in con_a:
        resnum_x, chain_x, atom_x, resnum_y, chain_y, atom_y, _ = e.split()
        try:
            resnum_x = str(numbering_dic[chain_x][int(resnum_x)])
            resnum_y = str(numbering_dic[chain_y][int(resnum_y)])
        except KeyError:
            # one of the residues present in this contact was not matched to the target
            continue
        a_con_l.append((resnum_x, chain_x, atom_x, resnum_y, chain_y, atom_y))

    b_con_l = [tuple(b.split()[:-1]) for b in con_b]

    fnat = float(len(set(a_con_l) & set(b_con_l))) / float(len(a_con_l))

    return fnat


def calc_lrmsd(prot_a, prot_b, numbering_dic, atoms):
    lrmsd = None

    # receptor = first chain
    chain_l = list(numbering_dic.keys())
    chain_l.sort()
    receptor_chain = chain_l[0]
    ligand_zone = {}
    for chain in numbering_dic:
        ligand_zone[chain] = []
        for ref_res in numbering_dic[chain]:
            target_res = numbering_dic[chain][ref_res]
            lzone = 'ZONE %s%s-%s%i:%s%i-%s%i' % (chain, ref_res, chain, ref_res, chain, target_res, chain, target_res)
            ligand_zone[chain].append(lzone)

    cmd = ''
    cmd += '\n'.join(ligand_zone[receptor_chain])
    cmd += '\n'
    cmd += 'FIT'
    cmd += '\n'
    for ligand in ligand_zone:
        if ligand != receptor_chain:
            l_tbw = ''
            for zone in ligand_zone[ligand]:
                l_tbw += ' R%s\n' % zone
            cmd += l_tbw[1:]
            cmd += '\n'
    cmd += 'ZONE CLEAR'
    cmd += '\n'

    lrms_cmd = 'refe %s\nmobi %s\nATOMS %s\n%s\nquit' % (prot_a, prot_b, atoms, cmd)
    open('lrmsd.dbg', 'w').write(cmd)

    out = run_profit(lrms_cmd)
    try:
        lrmsd = float(out[-1].split()[-1])
    except KeyError:
        print('Something went wrong when running PROFIT, check irmsd.dbg')
        exit()

    return lrmsd


def clean(prot_a, prot_b):
    pdb_l = [glob.glob('{}_*'.format(e.split('.pdb')[0])) for e in [prot_a, prot_b]]
    pdb_l = [x for xs in pdb_l for x in xs]
    for p in pdb_l:
        os.system('rm {}'.format(p))


def main():
    error_check = False
    for exe in ['profit', 'contact', 'lovoalign']:
        if not shutil.which(exe):
            print('ERROR: {} not found in $PATH'.format(exe))
            error_check = True

    if error_check:
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("prot_a", help="Reference protein")
    parser.add_argument("prot_b", help="Target protein")
    parser.add_argument("--cg", help="Use CG beads", action="store_true", default=False)

    args = parser.parse_args()
    if args.cg:
        atoms = 'BB*'
    else:
        atoms = 'CA,N,C,O'

    pa = args.prot_a
    pb = args.prot_b

    num_dic = align(pa, pb)

    contact_dic_a = identify_inteface(pa, 5.0)

    izone_list = retrieve_izone(contact_dic_a, num_dic)

    irmsd = calc_irmsd(pa, pb, atoms, izone_list)
    fnat = calc_fnat(pa, pb, num_dic)
    lrmsd = calc_lrmsd(pa, pb, num_dic, atoms)

    print('irmsd: {:.2f} lrmsd: {:.2f} fnat: {:.2f}'.format(irmsd, lrmsd, fnat))

    clean(pa, pb)


if __name__ == '__main__':
    main()
