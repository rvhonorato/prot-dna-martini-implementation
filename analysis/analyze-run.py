# the script that will evaluate all results in a docking run

import sys, os, glob, operator, subprocess, argparse, math
from operator import itemgetter
from itertools import groupby

#=========#

def get_contact_list(contactf):
    contact_list = []
    for l in open(contactf):
        resnumA,chainA,atomA,resnumB,chainB,atomB,distance = l.split()
        contact_list.append( ((int(resnumA),chainA,atomA), (int(resnumB),chainB,atomB)) )
        contact_list.append( ((int(resnumB),chainB,atomB), (int(resnumA),chainA,atomA)) )
    return contact_list

def fix_numbering(contact_list, offset_dic):
    # contact_list = conf_contacts
    edited_list = []
    for e in contact_list:
        resnumA, chainA, atomA = e[0]
        resnumB, chainB, atomB = e[1]

        eA = str(int(resnumA) + offset_dic[chainA]), chainA, atomA
        eB = str(int(resnumB) + offset_dic[chainB]), chainB, atomB

        edited_list.append( (eA, eB) )
    return edited_list

def fix_chain_segid(pdb_f):
    for l in open(pdb_f).readlines():
        if 'ATOM' in l[:4]:
            break
    #
    chain_check = bool(l[21].split())
    try:
        segid_check = bool(l[72:76].split())
    except IndexError:
        segid_check = False
    #
    if segid_check and not chain_check:
        # add chain
        # print('No Chain')
        chainf = pdb_f.replace('.pdb','_chain.pdb')
        cmd = '%s/tools/pdb_segid-to-chain %s' % (runf, pdb_f)
        run(cmd, chainf)
        os.rename(chainf, pdb_f)
    elif chain_check and not segid_check:
        # print('No Segid')
        # add segid
        segidf = pdb_f.replace('.pdb','_segid.pdb')
        cmd = '%s/tools/pdb_chain-to-segid %s' % (runf, pdb_f)
        run(cmd, segidf)
        os.rename(segidf, pdb_f)

def get_range(data):
    ### shamelessly copied from https://stackoverflow.com/a/2154437
    ranges = []
    for k, g in groupby(enumerate(data), lambda (i,x):i-x):
        group = map(itemgetter(1), g)
        ranges.append((group[0], group[-1]))
    return ranges
    ###

def retrieve_seqs(aln):
    # print aln
    aln_data = aln.readlines()
    header_idxs = [i for i, e in enumerate(aln_data) if '>' in e]
    seql = [i for i, e in enumerate(aln_data) if  not '>' in e]
    # seq_idx_list = [list(set(e)) for e in get_range(seql)]
    seq_idx_list = [range(r[0], r[1]+1) for r in get_range(seql)]

    seq_dic = {}
    for i, idx in enumerate(header_idxs):
        # print i, idx
        header = aln_data[idx]
        sequence = ''
        for sidx in seq_idx_list[i]:
            sequence += aln_data[sidx]
        #
        chain = header.split()[0].split('_')[-1]
        seq_dic[chain] = ''.join(sequence.split())
        # print header, sequence
    return seq_dic

def retrieve_seqs2(fastaf):

    aln_data = open(fastaf).readlines()
    header_idxs = [i for i, e in enumerate(aln_data) if '>' in e]
    seql = [i for i, e in enumerate(aln_data) if  not '>' in e]
    seq_idx_list = [range(r[0], r[1]+1) for r in get_range(seql)]

    seq_dic = {}
    for i, idx in enumerate(header_idxs):
        header = aln_data[idx]
        sequence = ''
        for sidx in seq_idx_list[i]:
            sequence += aln_data[sidx]

        chain = header.split()[0].split('|')[-1]
        seq_dic[chain] = ''.join(sequence.split())
    return seq_dic

def run(cmd, outputf):
    with open(outputf, "w") as f:
        process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
        process.wait()

def find_key(dic, val):
    '''return the key of dictionary dic given the value'''
    return [k for k, v in dic.iteritems() if v == val][0]


def get_contact_list(contactf):
    contact_list = []
    for l in open(contactf):
        resnumA,chainA,atomA,resnumB,chainB,atomB,distance = l.split()
        contact_list.append( ((int(resnumA),chainA,atomA), (int(resnumB),chainB,atomB)) )
        contact_list.append( ((int(resnumB),chainB,atomB), (int(resnumA),chainA,atomA)) )
    return contact_list

# def rename_nuc(pdb):
# 	d = {'A': '  A','C': '  C','T': '  T','G': '  G','U': '  U'}
# 	out = open('temp.pdb','w')
# 	for l in open(pdb):
# 		if 'ATOM' in l[:4]:
# 			try:
# 				res = l[17:20].split()[0]
# 				new_res = d[res]
# 				nl =  l[:17] + d[res] + l[20:]
# 			except:
# 				nl = l
# 			out.write('%s' % nl)
# 	out.close()
# 	print pdb
# 	exit()
# 	return 'temp.pdb'



def cluster_stats(score_f, irmsd_f,cluster_f):
    score_dic = dict([(i+1,float(l.split()[-2])) for i, l in enumerate(open(score_f))])
    model_dic = dict([(i+1,l.split()[0].split(':')[-1][:-1]) for i, l in enumerate(open(score_f))])
    irmsd_dic = dict([(l.split()[0], float(l.split()[1])) for l in open(irmsd_f).readlines()[1:]])

    c_dic = {}
    cluster_model_dic = {}
    for c in open(cluster_f):
        cluster_idx = int(c.split()[1])
        center = c.split()[3]
        top4 = map(int, c.split()[4:8])
        #
        mean_cluster_score = sum([score_dic[e] for e in top4]) / 4.0
        c_dic[cluster_idx] = mean_cluster_score
        cluster_model_dic[cluster_idx] = map(int, c.split()[3:])

    # sort clusters
    sorted_c_dic = sorted(c_dic.items(), key=operator.itemgetter(1))

    # get models
    output = ''
    for i, c in enumerate(sorted_c_dic):
        modelid_list = cluster_model_dic[c[0]]
        modelname_list = [model_dic[mid] for mid in modelid_list]
        #
        score_l = [score_dic[mid] for mid in modelid_list]
        irmsd_l = [irmsd_dic[m] for m in modelname_list]
        top4_irmsdl = [irmsd_dic[m] for m in modelname_list[1:5]] # index 0 is the cluster center according to FCC
        mean_irmsd = sum(irmsd_l) / len(irmsd_l)
        mean_score = sum(score_l) / len(score_l)
        top4_irmsd = sum(top4_irmsdl) / len(top4_irmsdl)
        #
        output += 'Top_%i\tCluster_%i\ttop4_score: %.2f\tmean_score: %.5f\ttop4_irmsd: %.2f\tmean_irsmd: %.2f\n%s\n' % (i+1, c[0], c[1], mean_score, top4_irmsd, mean_irmsd, ','.join(modelname_list))

    return output

def validate_pdbl(pdbl):
    l = []
    for pdb in pdbl:
        if os.path.isfile(pdb+'.gz'):
            os.system('gunzip %s' % pdb)
            # l.append(pdb+'.gz')
            # else:
        l.append(pdb)
    return l


# global haddocktools_path
global runf
# haddocktools_path = '/Users/rvhonorato/tools'
haddocktools_path = os.environ["HADDOCKTOOLS"]
clustalo_exe = '/home/rodrigo/clustal-omega'
fnat_distance_threshold = 5.0

#======#

parser = argparse.ArgumentParser()

parser.add_argument("pdbf", type=str,
                    help="Reference PDB (xtal)")

parser.add_argument("runf", type=str,
                    help="run name (ex. run1)")

parser.add_argument("--aa", help="do AA analysis",
                    action="store_true")

args = parser.parse_args()

pdbf = args.pdbf
pdbf_cg = pdbf.replace('.pdb','_cg.pdb')
pdb_name = pdbf.split('.pdb')[0]

runf = args.runf

path = os.getcwd()
# path = None


# check if it needs chain/segid fixing
fix_chain_segid(pdbf)
if not args.aa:
    fix_chain_segid(pdbf_cg)
# fix_terms(pdbf)7

# get pdb lists
it0_l = ['%s/structures/it0/%s' % (runf,p.split()[0]) for p in open('%s/structures/it0/file.nam' % (runf)).readlines() if 'pdb' in p]
it1_l = ['%s/structures/it1/%s' % (runf,p.split()[0]) for p in open('%s/structures/it1/file.nam' % (runf)).readlines() if 'pdb' in p]
water_l = ['%s/structures/it1/water/%s' % (runf,p.split()[0]) for p in open('%s/structures/it1/water/file.nam' % (runf)).readlines() if 'pdb' in p]

# it0_l = ['%s/%s/structures/it0/%s' % (path,runf,p.split()[0]) for p in open('%s/%s/structures/it0/file.nam' % (path,runf)).readlines() if 'pdb' in p]
# it1_l = ['%s/%s/structures/it1/%s' % (path,runf,p.split()[0]) for p in open('%s/%s/structures/it1/file.nam' % (path,runf)).readlines() if 'pdb' in p]
# water_l = ['%s/%s/structures/it1/water/%s' % (path,runf,p.split()[0]) for p in open('%s/%s/structures/it1/water/file.nam' % (path,runf)).readlines() if 'pdb' in p]


it0_l = validate_pdbl(it0_l)
it1_l = validate_pdbl(it1_l)
water_l = validate_pdbl(water_l)

it0_l.sort()
it1_l.sort()
water_l.sort()

# it0_l = glob.glob('%s/%s/structures/it0/*pdb' % (path, runf))
# it1_l = glob.glob('%s/%s/structures/it1/*pdb' % (path, runf))
# water_l = glob.glob('%s/%s/structures/it1/water/*pdb' % (path, runf))

# atoms to be used during i-rmsd calculation
if args.aa:
    stage_ref_dic = {
        'it0':   [it0_l, pdbf, ("CA,C,N,O,P,C1,C9")],
        'it1':   [it1_l, pdbf, ("CA,C,N,O,P,C1,C9")],
        'water': [water_l, pdbf, ("CA,C,N,O,P,C1,C9")]
    }
else:
    stage_ref_dic = {
        'it0':   [it0_l, pdbf_cg, ("BB,BB1,BB2,BB3")],
        'it1':   [it1_l, pdbf_cg, ("BB,BB1,BB2,BB3")],
        'water': [water_l, pdbf, ("CA,C,N,O,P,C1,C9")]
}

# create and populate result dictionary
result_dic = {}
for stage in stage_ref_dic:
    result_dic[stage] = {}
    pdb_l = stage_ref_dic[stage][0]
    for pdb in pdb_l:
        result_dic[stage][pdb] = {'fnat': float('nan'), 'irms': float('nan'), 'lrms': float('nan'), 'total': float('nan'),
        'bonds': float('nan'), 'angles': float('nan'), 'improper': float('nan'), 'dihe': float('nan'), 'vdw': float('nan'),
        'elec': float('nan'), 'air': float('nan'), 'cdih': float('nan'), 'coup': float('nan'), 'rdcs': float('nan'),
        'vean': float('nan'), 'dani': float('nan'), 'xpcs': float('nan'), 'rg': float('nan'),
        'bsa' : float('nan'),
        'desolv' : float('nan'),
        'binding' : float('nan')}

#=========================================================================================#
## Numbering
#=========================================================================================#
# create numbering dic on the fly
print '> Matching numbering via sequence alignment'

# Fetch a model from the run
decoy = stage_ref_dic['water'][0][0]

if not os.path.isfile(decoy) and not os.path.isfile(decoy + '.gz'):
    exit()
elif os.path.isfile(decoy):
    os.system('cp %s .' % decoy)
else:
    decoy = decoy + 'gz'
    os.system('cp %s .' % decoy)
    os.system('gunzip %s' % decoy)

decoy_name = decoy.split('/')[-1].split('.pdb')[0]

os.system('cp %s .' % decoy)

chain_list = list(set([l[21] for l in open(pdbf).readlines() if 'ATOM' in l [:4]]))
target_chain_dic = dict([(c, []) for c in chain_list])

# split it by segid
os.system('python /home/rodrigo/pdb-tools/pdbtools/pdb_splitseg.py %s.pdb' % decoy_name)
# os.system('pdb_splitseg %s.pdb' % decoy_name)

# put in the dictionary
pdb_dic = dict([(c.split('_')[-1].split('.pdb')[0], c) for c in glob.glob('%s_*pdb*' % decoy_name)])


ref_seqf = 'reference.fasta'
# cmd = 'python /home/rodrigo/pdb-tools/pdb_toseq.py %s' % pdbf
# cmd = 'pdb_toseq %s' % pdbf
cmd = 'python /home/rodrigo/pdb-tools/pdbtools/pdb_tofasta.py -multi %s' % pdbf
run(cmd, ref_seqf)
ref_seq_dic = retrieve_seqs2(ref_seqf)

len_dic = {}
numbering_dic = {}
for chain in pdb_dic:

    open('ref.fasta','w').write('>ref\n%s\n' % ref_seq_dic[chain])

    pdb = pdb_dic[chain]
    seqf = pdb.replace('.pdb','.fasta')
    # cmd = 'python /home/rodrigo/pdb-tools/pdb_toseq.py %s' % pdb
    cmd = 'python /home/rodrigo/pdb-tools/pdbtools/pdb_tofasta.py %s' % pdb
    run(cmd, seqf)

    # prepare alignment
    aln_outf = '%s.aln' % chain
    os.system('cat ref.fasta %s > seqs.fasta' % seqf)
    cmd = '%s -i seqs.fasta --outfmt=clu --resno --wrap=9000 --force' % clustalo_exe
    print cmd
    run(cmd, aln_outf)

    aln_list = []
    # identity
    for l in open(aln_outf):
        if 'ref' in l:
            aln_list.append(l.split()[1])
        elif 'PDB' in l:
        # elif pdb.split('.')[0] in l:
            aln_list.append(l.split()[1])

    ref_seq_aln = aln_list[0]
    ubound_seq_aln = aln_list[1]

    ref_res_l = list(set([int(l[22:26]) for l in open(pdbf).readlines() if 'ATOM' in l[:4] and chain == l[21]]))
    # chain_res_l = list(set([int(l[22:26]) for l in open(pdb).readlines() if 'ATOM' in l[:4] and chain == l[21]])) # chain
    chain_res_l = list(set([int(l[22:26]) for l in open(pdb).readlines() if 'ATOM' in l[:4] and chain == l[72:76][0]])) # segid

    ref_res_dic = dict([(i+1, e) for i, e in enumerate(ref_res_l)])
    chain_res_dic = dict([(i+1, e) for i, e in enumerate(chain_res_l)])

    counterA = 0
    counterB = 0
    offset = 0
    numbering_list = []

    for position, aln in enumerate(zip(ref_seq_aln, ubound_seq_aln)):
        #
        resA = aln[0]
        resB = aln[1]
        #
        if resA != '-':
            counterA +=1
        if resB != '-':
            counterB +=1
        #
        if not '-' in aln:
            resnumA = ref_res_dic[counterA]
            resnumB = chain_res_dic[counterB]
            # print position, aln, counterA, counterB, resnumA, resnumB
            # exit()
            if resA != resB:
                print 'WARNING: Reference chain %s aa %s position %i does not match target chain %s aa %s' % (chain, resA, i, chain, resB)
            else:
                numbering_list.append((resnumA, resnumB))

    numbering_dic[chain] = dict(numbering_list)


size_l = [(c, len(numbering_dic[c])) for c in numbering_dic ]
size_l.sort()
receptor_chain = size_l[0][0]

#=========================================================================================#
## Interface RMSD
#=========================================================================================#

print '> Calculating i-rmsd'
# define contact for AA and for CG
izone_dic = {}
for ref in [pdbf, pdbf_cg]:
    distance_threshold = 10.
    ref_contactf = ref.split('.')[0] + '_%i.contacts' % distance_threshold
    cmd = '%s/tools/contact %s %i' % (runf, ref, distance_threshold)
    print(cmd)
    run(cmd, ref_contactf)

    contact_list = []
    for l in open(ref_contactf):
        resnumA,chainA,atomA,resnumB,chainB,atomB,distance = l.split()
        contact_list.append( (chainA,int(resnumA)) )
        contact_list.append( (chainB,int(resnumB)) )

    contact_list = list(set(contact_list))
    contact_list.sort()

    # create and populate a dictionary
    contact_dic = dict([(e[0], []) for e in contact_list])
    for e in contact_list:
        contact_dic[e[0]].append(e[1])

    # match izones
    out = open('%s.izone' % ref.split('.pdb')[0],'w')
    izone_l = []

    ######################
    # new method

    # crate a bound-unbound reference of the residues that are in contact
    for chain in contact_dic:
        ref_dic = {}
        for bound_res in contact_dic[chain]:
            try:
                ub = numbering_dic[chain][bound_res]
                ref_dic[bound_res] = ub
            except:
                pass

        # define the bound ranges ex (1-20)
        for bound_range in get_range(ref_dic.keys()):
            # for each bound range
            #  check which is the unbound range that matches
            unbound_res_l = []
            for bound_res in range(bound_range[0], bound_range[1]+1):
                unbound_res = ref_dic[bound_res]
                unbound_res_l.append(ref_dic[bound_res])

            # use unbound_res_l to build zones
            for unbound_range in get_range(unbound_res_l):
                bound_res_l = []
                for unbound_res in range(unbound_range[0],unbound_range[1]+1):
                    # find what it the bound res that correspond to this unbound
                    bound_res_l.append(find_key(ref_dic, unbound_res))
                #
                rangeA = get_range(bound_res_l)[0] # bound
                rangeB = unbound_range
                #
                # print chain, rangeA, rangeB
                #
                izone_str = 'ZONE %s%i-%s%i:%s%i-%s%i' % (chain, rangeA[0], chain, rangeA[1], chain, rangeB[0], chain, rangeB[1])
                # print izone_str
                izone_l.append(izone_str)
                out.write(izone_str)
    # exit()
    ######################

    ######################
    # old method
    # for chain in contact_dic:
    # 	for bound_res in contact_dic[chain]:
    # 		try:
    # 			unbound_res = numbering_dic[chain][bound_res]
    # 			izone_l.append('ZONE %s%i-%s%i:%s%i-%s%i' % (chain, bound_res, chain, bound_res, chain, unbound_res, chain,unbound_res))
    # 			out.write('ZONE %s%i-%s%i:%s%i-%s%i\n' % (chain, bound_res, chain, bound_res, chain, unbound_res, chain,unbound_res))
    # 			# print 'ZONE %s%i-%s%i:%s%i-%s%i' % (chain, bound_res, chain, bound_res, chain, unbound_res, chain,unbound_res)
    # 		except:
    # 			print 'Res %i not found in unbound' % bound_res
    ######################

    out.close()
    izone_dic[ref] = izone_l

for stage in stage_ref_dic:
    # stage = 'it0'
    ####
    pdb_l = stage_ref_dic[stage][0]
    ref = stage_ref_dic[stage][1]
    atoms = stage_ref_dic[stage][2]
    izone_l = izone_dic[ref]

    print '>> %s' % stage

    # prepare structural input
    irms_dic = {}
    # counter = 0
    for conformation in pdb_l:

        # check if gz
        if '.gz' in conformation:
            os.system('gunzip %s' % conformation)
            conformation = conformation.split('.gz')[0]
        #####
        # fix chain
        fix_chain_segid(conformation)

        #####################################
        # WARNING                           #
        # This will remove H5T/H3T atoms!   #
        # cmd = 'bash /home/rodrigo/Nostromo/scripts/fix_term.sh %s' % conformation
        # run(cmd, 'fix')
        #####################################

        # #####################################
        # # WARNING                           #
        # # This will rename nucleotides      #
        # cmd = 'bash /home/rodrigo/Nostromo/scripts/rename_nuc.sh %s' % conformation
        # run(cmd, 'rename')
        # #####################################

        # _ = rename_nuc(conformation)

        # prepare cmd for PROFIT
        cmd = 'refe %s\nmobi %s\nATOMS %s\nZONE CLEAR\n%s\nstatus\nFIT\nquit' % (ref, conformation, atoms, '\n'.join(izone_l))

        # save this for debug
        open('irmsd_%s.dbg' % stage,'w').write(cmd)
        # open('idbg_%i' % counter,'w').write(cmd)
        # if counter == 2:
        # 	exit()
        # counter += 1

        # run!
        output = os.popen('echo "%s" | profit' % cmd) # if this fails, check the terminal atoms..

        # parse result
        # error_check = False
        # for l in output:
        #     if 'Error':
        #         print('ERROR, run $ profit < irmsd.dbg')
        #         exit()

        result = [l for l in output if 'RMS:' in l][0]

        irms = float(result.split()[-1])

        irms_dic[conformation] = irms
        result_dic[stage][conformation]['irms'] = irms

    #
    if stage == 'water':
        outputf = '%s/%s/structures/it1/%s/i-RMSD-sorted.dat' % (path, runf, stage)
    else:
        outputf = '%s/%s/structures/%s/i-RMSD-sorted.dat' % (path, runf, stage)
    #
    irms_out = open(outputf,'w')
    irms_out.write('#struc i-RMSD\n')
    sorted_irms_dic = sorted(irms_dic.items(), key=operator.itemgetter(1))
    for e in sorted_irms_dic:
        conformation = e[0]
        pdb_name = conformation.split('/')[-1]
        irms = e[1]
        irms_out.write('%s %.3f\n' % (pdb_name, irms))
    irms_out.close()
    #
    # os.system('cp %s %s' % (outputf, outputf.replace('.dat', '-sorted.dat')))


#=========================================================================================#
## Ligand RMSD
#=========================================================================================#

print '> Calculating l-rmsd'

ligand_zone = {}
for chain in numbering_dic:
	ligand_zone[chain] = []
	for bound_res in numbering_dic[chain]:
		unbound_res = numbering_dic[chain][bound_res]
		#
		ligand_zone[chain].append('ZONE %s%s-%s%i:%s%i-%s%i' % (chain, bound_res, chain, bound_res, chain, unbound_res, chain, unbound_res))

# generate command
lrms_cmd = ''
lrms_cmd += '\n'.join(ligand_zone[receptor_chain])
lrms_cmd += '\n'
lrms_cmd += 'FIT'
lrms_cmd += '\n'
for ligand in ligand_zone:
	if ligand != receptor_chain:
		l_tbw = ''
		for zone in ligand_zone[ligand]:
			l_tbw += ' R%s\n' % zone
		lrms_cmd += l_tbw[1:]
		lrms_cmd += '\n'
lrms_cmd += 'ZONE CLEAR'
lrms_cmd += '\n'

# ready?
for stage in stage_ref_dic:
	# print '>> %s' % stage

	pdb_l = stage_ref_dic[stage][0]
	ref = stage_ref_dic[stage][1]
	atoms = stage_ref_dic[stage][2]

	lrms_dic = {}
	for conformation in pdb_l:

		# segid_output = 'segid.temp'
		fix_chain_segid(conformation)

		# os.system('%s/pdb_segid-to-chain %s > %s' % (haddocktools_path, conformation, segid_output))
		# os.system('cp segid.temp %s' % conformation)
		cmd = 'refe %s\nmobi %s\nATOMS %s\n%s\nquit' % (ref, conformation, atoms, lrms_cmd)

		output = os.popen('echo "%s" | profit' % cmd)

		# parse result
		result = [l for l in output if 'RMS' in l][-1]
		lrms = float(result.split()[-1])

		lrms_dic[conformation] = lrms
		result_dic[stage][conformation]['lrms'] = lrms
		#
		# os.system('rm %s' % segid_output)

	if stage == 'water':
		outputf = '%s/structures/it1/%s/l-RMSD.dat' % (runf, stage)
	else:
		outputf = '%s/structures/%s/l-RMSD.dat' % (runf, stage)

	#
	lrms_out = open(outputf,'w')
	lrms_out.write('#struc l-RMSD\n')
	sorted_lrms_dic = sorted(lrms_dic.items(), key=operator.itemgetter(1))
	for e in sorted_lrms_dic:
		conformation = e[0]
		pdb_name = conformation.split('/')[-1]
		lrms = e[1]
		lrms_out.write('%s %.3f\n' % (conformation, lrms))
	lrms_out.close()
	#
	os.system('cp %s %s' % (outputf, outputf.replace('.dat', '-sorted.dat')))

#=========================================================================================#
## Fnat
#=========================================================================================#

print '> Calculating fnat (%.2f A)' % fnat_distance_threshold

# define contact for AA and for CG
contact_dic = {}
for ref in [pdbf, pdbf_cg]:
    #
    contact_outf = ref.replace('.pdb', '.contacts')
    cmd = '%s/tools/contact %s %i' % (runf, ref, fnat_distance_threshold)
    run(cmd, contact_outf)

    bound_contact_list = get_contact_list(contact_outf)

    # check numbering and ignore contacts seen only in reference
    fixed_contact_list = []
    for contact in bound_contact_list:
        # print contact
        bound_resA = contact[0][0]
        bound_resB = contact[1][0]
        #
        chainA = contact[0][1]
        chainB = contact[1][1]
        #
        atomA = contact[0][2]
        atomB = contact[1][2]
        #
        try:
            unbound_resA = numbering_dic[chainA][bound_resA]
        except:
            unbound_resA = None

        #
        try:
            unbound_resB = numbering_dic[chainB][bound_resB]
        except:
            unbound_resB = None

        if unbound_resA and unbound_resB:
            new_contact = ( (unbound_resA, chainA, atomA), (unbound_resB, chainB, atomB) )
            fixed_contact_list.append(new_contact)
        else:
            pass
            # print contact, 'discarded, not found on decoy'
    #
    contact_dic[ref] = fixed_contact_list


for stage in stage_ref_dic:

    pdb_l = stage_ref_dic[stage][0]
    ref = stage_ref_dic[stage][1]

    print '>> stage %s' % stage

    fnat_dic = {}
    for conformation in pdb_l:
        ###
        fix_chain_segid(conformation)

        contact_outf = conformation.replace('.pdb', '.contacts')
        cmd = '%s/tools/contact %s %i' % (runf, conformation, fnat_distance_threshold)
        run(cmd, contact_outf)

        conformation_contacts = get_contact_list(contact_outf)

        fnat = float(len(set(contact_dic[ref]) & set(conformation_contacts))) / float(len(contact_dic[ref]))

        fnat_dic[conformation] = fnat
        result_dic[stage][conformation]['fnat'] = fnat

    if stage == 'water':
        outputf = '%s/structures/it1/%s/file.nam_fnat' % (runf, stage)
    else:
        outputf = '%s/structures/%s/file.nam_fnat' % (runf, stage)
    #
    fnat_out = open(outputf,'w')
    sorted_fnat_dic = sorted(fnat_dic.items(), key=operator.itemgetter(1))
    sorted_fnat_dic.reverse()
    for e in sorted_fnat_dic:
        conformation = e[0]
        pdb_name = conformation.split('/')[-1]
        fnat = e[1]
        fnat_out.write('%s %.3f\n' % (pdb_name, fnat))
    fnat_out.close()
    #
    # os.system('cp %s %s' % (outputf, outputf.replace('.dat', '-sorted.dat')))


#=========================================================================================#
# Clustering
#=========================================================================================#

print '> Analyzing clusters'

# water
if os.path.isfile('%s/%s/structures/it1/water/analysis/cluster.out.gz' % (path, runf)):
    water_clusterf = '%s/%s/structures/it1/water/analysis/cluster.out.gz' % (path, runf)
elif os.path.isfile('%s/%s/structures/it1/water/analysis/cluster.out' % (path, runf)):
    water_clusterf = '%s/%s/structures/it1/water/analysis/cluster.out' % (path, runf)
else:
    water_clusterf = False

# it1
if os.path.isfile('%s/%s/structures/it1/analysis/cluster.out.gz' % (path, runf)):
    it1_clusterf = '%s/%s/structures/it1/analysis/cluster.out.gz' % (path, runf)
elif os.path.isfile('%s/%s/structures/it1/analysis/cluster.out' % (path, runf)):
    it1_clusterf = '%s/%s/structures/it1/analysis/cluster.out' % (path, runf)
else:
    it1_clusterf = False

if water_clusterf:
    if 'gz' in water_clusterf:
        os.chdir('%s/%s/structures/it1/water/analysis/' % (path, runf))
        os.system('gunzip cluster.out.gz')

    os.chdir('%s/%s/structures/it1/water/' % (path, runf))
    # os.system('%s/tools/ana_clusters.csh -best 4 analysis/cluster.out' % runf)
    os.system('%s/ana_clusters.csh -best 4 analysis/cluster.out' % haddocktools_path)
    os.chdir(path)

    score_f = '%s/%s/structures/it1/water/file.list' % (path, runf)
    cluster_f = '%s/%s/structures/it1/water/analysis/cluster.out' % (path, runf)
    irmsd_f = '%s/%s/structures/it1/water/i-RMSD-sorted.dat' % (path, runf)

    water_cluster_statf = open('water_cluster.dat','w')
    tbw = cluster_stats(score_f, irmsd_f,cluster_f)
    water_cluster_statf.write(tbw)
    water_cluster_statf.close()

if it1_clusterf:
    if 'gz' in it1_clusterf:
        os.chdir('%s/%s/structures/it1/analysis/' % (path, runf))
        os.system('gunzip cluster.out.gz')

    os.chdir('%s/%s/structures/it1/' % (path, runf))
    # os.system('%s/tools/ana_clusters.csh -best 4 analysis/cluster.out' % runf)
    os.system('%s/ana_clusters.csh -best 4 analysis/cluster.out' % haddocktools_path)

    score_f = '%s/%s/structures/it1/file.list' % (path, runf)
    cluster_f = '%s/%s/structures/it1/analysis/cluster.out' % (path, runf)
    irmsd_f = '%s/%s/structures/it1/i-RMSD-sorted.dat' % (path, runf)

    it1_cluster_statf = open('it1_cluster.dat','w')
    tbw = cluster_stats(score_f, irmsd_f,cluster_f)
    it1_cluster_statf.write(tbw)
    it1_cluster_statf.close()

os.chdir(path)


#=========================================================================================#
# Output
#=========================================================================================#

haddock_score_dic = {}
for stage in stage_ref_dic:
    # get haddock score
    haddock_score_dic[stage] = {}

    if stage == 'water':
        haddock_s_f = '%s/structures/it1/%s/file.list' % (runf, stage)
    else:
        haddock_s_f = '%s/structures/%s/file.list' % (runf,  stage)

    for l in open(haddock_s_f):
        pdb_name = l.split(':')[-1].split()[0].split('"')[0]
        score = float(l.split()[2])
        # if math.isnan(score):
        # 	print l
        # full_name = 'run2/structures/%s/%s'% (stage, pdb_name)
        full_name = haddock_s_f.replace('file.list', pdb_name)
        haddock_score_dic[stage][full_name] = score

    # get energies and etc
    pdb_l = stage_ref_dic[stage][0]
    for conformation in pdb_l:
        data = open(conformation).readlines()

        energies_l = map(float, data[6].split(':')[-1].split(','))
        total, bonds, angles, improper, dihe, vdw, elec, air, cdih, coup, rdcs, vean, dani, xpcs, rg = energies_l

        bsa = float(data[31].split(':')[-1])
        binding = float(data[29].split(':')[-1])
        desolv = float(data[26].split(':')[-1])

        result_dic[stage][conformation]['total'] = total
        result_dic[stage][conformation]['bonds'] = bonds
        result_dic[stage][conformation]['angles'] = angles
        result_dic[stage][conformation]['improper'] = improper
        result_dic[stage][conformation]['dihe'] = dihe
        result_dic[stage][conformation]['vdw'] = vdw
        result_dic[stage][conformation]['elec'] = elec
        result_dic[stage][conformation]['air'] = air
        result_dic[stage][conformation]['cdih'] = cdih
        result_dic[stage][conformation]['coup'] = coup
        result_dic[stage][conformation]['rdcs'] = rdcs
        result_dic[stage][conformation]['vean'] = vean
        result_dic[stage][conformation]['dani'] = dani
        result_dic[stage][conformation]['xpcs'] = xpcs
        result_dic[stage][conformation]['rg'] = rg
        result_dic[stage][conformation]['bsa'] = bsa
        result_dic[stage][conformation]['desolv'] = desolv
        result_dic[stage][conformation]['binding'] = binding


for stage in result_dic:
    # out = open('%s/%s.dat' % (runf, stage),'w')
    out = open('%s.dat' % stage, 'w')
    out.write('stage\tpdb_name\trank\tscore\tfnat\tlrms\tirms\tbinding\tdesolv\tbsa\ttotal\tbonds\tangles\timproper\tdihe\tvdw\telec\tair\tcdih\tcoup\trdcs\tvean\tdani\txpcs\trg\n')

    sorted_haddock_score_list = sorted(haddock_score_dic[stage].items(), key=operator.itemgetter(1))
    for i, e in enumerate(sorted_haddock_score_list):

        conformation = e[0]
        rank = i+1

        fnat = result_dic[stage][conformation]['fnat']
        lrms = result_dic[stage][conformation]['lrms']
        irms = result_dic[stage][conformation]['irms']

        total = result_dic[stage][conformation]['total']
        bonds = result_dic[stage][conformation]['bonds']
        angles = result_dic[stage][conformation]['angles']
        improper = result_dic[stage][conformation]['improper']
        dihe = result_dic[stage][conformation]['dihe']
        vdw = result_dic[stage][conformation]['vdw']
        elec = result_dic[stage][conformation]['elec']
        air = result_dic[stage][conformation]['air']
        cdih = result_dic[stage][conformation]['cdih']
        coup = result_dic[stage][conformation]['coup']
        rdcs = result_dic[stage][conformation]['rdcs']
        vean = result_dic[stage][conformation]['vean']
        dani = result_dic[stage][conformation]['dani']
        xpcs = result_dic[stage][conformation]['xpcs']
        rg = result_dic[stage][conformation]['rg']
        #
        bsa = result_dic[stage][conformation]['bsa']
        desolv = result_dic[stage][conformation]['desolv']
        binding = result_dic[stage][conformation]['binding']
        #
        haddock_score = haddock_score_dic[stage][conformation]
        #
        out.write('%s\t%s\t%i\t%.4f\t%.3f\t%.2f\t%.2f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\n' % (stage, conformation, rank, haddock_score, fnat, lrms, irms,
            binding,
            desolv,
            bsa,
            total, bonds, angles, improper, dihe, vdw, elec, air, cdih, coup, rdcs, vean, dani, xpcs, rg))

    out.close()
    pass
    #

# write i-RMSD.dat > sorted by haddock score
pass

for stage in result_dic:
    if stage == 'water':
        outputf_name = '%s/structures/it1/%s/i-RMSD.dat' % (runf, stage)
    else:
        outputf_name = '%s/structures/%s/i-RMSD.dat' % (runf,  stage)

    outputf = open(outputf_name, 'w')

    sorted_haddock_score_list = sorted(haddock_score_dic[stage].items(), key=operator.itemgetter(1))

    for i, e in enumerate(sorted_haddock_score_list):

        conformation = e[0].split('/')
        irms = result_dic[stage][e[0]]['irms']

        outputf.write('%s %.3f' % (conformation, irms))

    outputf.close()




# done (:







