# re-arrange input pdb chains so it matches the reference structure
import sys
import subprocess
import operator
import os

clustalo_exe = '/home/rodrigo/clustal-omega'
if not os.path.isfile(clustalo_exe):
    print('ClustalO not found')
    exit()


def load_seq(prot):
    aa_dic = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLU': 'E',
              'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W',
              'TYR': 'Y', 'VAL': 'V', 'DC': 'C',
              'DA': 'A', 'DG': 'G', 'DT': 'T',
              'ADE': 'A', 'THY':'T', 'GUA': 'G', 'CYT': 'C'}
    seq_dic = {}
    for l in open(prot):
        if 'ATOM' in l[:4]:
            segment_id = l[72:76].strip()
            resnum = int(l[22:26])
            resname = l[17:20].split()[0]
            try:
                _ = seq_dic[segment_id]
            except KeyError:
                seq_dic[segment_id] = {}
            try:
                name = aa_dic[resname]
            except KeyError:
                name = 'X'
            seq_dic[segment_id][resnum] = name
    return seq_dic


def main():

    ref = sys.argv[1]
    target = sys.argv[2]

    ref_seq_dic = load_seq(ref)
    target_seq_dic = load_seq(target)

    ident_dic = {}
    for segid_x in ref_seq_dic:
        ident_dic[segid_x] = {}
        for segid_y in target_seq_dic:
            ref_seq = ''.join(list(ref_seq_dic[segid_x].values()))
            target_seq = ''.join(list(target_seq_dic[segid_y].values()))

            open('seq.fasta','w').write(f'>ref\n{ref_seq}\n>target\n{target_seq}\n')

            cmd = f'{clustalo_exe} -i seq.fasta --outfmt=clu --resno --wrap=9000 --force'
            p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = p.communicate()

            ident = out[0].decode('utf-8').count('*') / float(len(ref_seq))
            ident_dic[segid_x][segid_y] = ident

    change_dic = {}
    for ref_segid in ident_dic:
        sorted_d = sorted(ident_dic[ref_segid].items(), key=operator.itemgetter(1))
        sorted_d.reverse()
        target_segid, ident = sorted_d[0]
        change_dic[target_segid] = ref_segid
        # print(ref_segid, target_segid, ident)

    for l in open(target):
        if 'ATOM' in l[:4]:
            segment_id = l[72:76].strip()
            new_segment_id = change_dic[segment_id]
            print(l[:21] + f'{new_segment_id}' + l[22:72] + f'{new_segment_id}   ')


if __name__ == '__main__':
    main()
