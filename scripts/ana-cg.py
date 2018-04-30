# the script that will evaluate all results in a docking run

import sys, os, glob, operator, subprocess, argparse
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
#
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
		chainf = pdb_f.replace('.pdb','_chain.pdb')
		cmd = '%s/pdb_segid-to-chain %s' % (haddocktools_path, pdb_f)
		run(cmd, chainf)
		os.rename(chainf, pdb_f)
	elif chain_check and not segid_check:
		# add segid
		segidf = pdb_f.replace('.pdb','_segid.pdb')
		cmd = '%s/pdb_chain-to-segid %s' % (haddocktools_path, pdb_f)
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

def run(cmd, outputf):
	with open("./%s" % outputf, "w") as f:
	    process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
	    process.wait()


global haddocktools_path
# haddocktools_path = '/Users/rvhonorato/tools'
haddocktools_path = os.environ["HADDOCKTOOLS"]
#======#

parser = argparse.ArgumentParser()

parser.add_argument("pdbf", type=str,
                    help="Reference PDB (xtal)")

parser.add_argument("runf", type=str,
                    help="run number (ex. run1)")

parser.add_argument("--aa", help="do AA analysis",
                    action="store_true")

args = parser.parse_args()

pdbf = args.pdbf
# pdbf = sys.argv[1]
pdbf_cg = pdbf.replace('.pdb','_cg.pdb')

# runf = sys.argv[2]
runf = args.runf

pdb_name = pdbf.split('.pdb')[0]

# check if it needs chain/segid fixing
fix_chain_segid(pdbf)
fix_chain_segid(pdbf_cg)

# get pdb lists
it0_l = glob.glob('%s/structures/it0/*pdb' % runf)
it1_l = glob.glob('%s/structures/it1/*pdb' % runf)
water_l = glob.glob('%s/structures/it1/water/*pdb' % runf)

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

# create and populate residue lists
result_dic = {}
for stage in stage_ref_dic:
	result_dic[stage] = {}
	# pdb_l = 
	pdb_l = stage_ref_dic[stage][0] 
	for pdb in pdb_l:
		result_dic[stage][pdb] = {'fnat': float('nan'), 'irms': float('nan'), 'lrms': float('nan'), 'total': float('nan'), 
		'bonds': float('nan'), 'angles': float('nan'), 'improper': float('nan'), 'dihe': float('nan'), 'vdw': float('nan'), 
		'elec': float('nan'), 'air': float('nan'), 'cdih': float('nan'), 'coup': float('nan'), 'rdcs': float('nan'), 
		'vean': float('nan'), 'dani': float('nan'), 'xpcs': float('nan'), 'rg': float('nan'),
		'buried' : float('nan'),
		'desolv' : float('nan'),
		'binding' : float('nan')}


numbering_dic = {}
for f in glob.glob('*numbering.ref'):
	# open(f).readlines()
	chain = f.split('-')[0]
	numbering_dic[chain] = dict([map(int, a.split(',')) for a in open(f)])

size_l = [(c, len(numbering_dic[c])) for c in numbering_dic ]
size_l.sort()
receptor_chain = size_l[0][0]

#=========================================================================================#
## Interface RMSD
#=========================================================================================#

print '> i-rmsd'
# define contact for AA and for CG
izone_dic = {}
for ref in [pdbf, pdbf_cg]:
	distance_threshold = 10.
	ref_contactf = ref.split('.')[0] + '_%i.contacts' % distance_threshold
	cmd = '%s/contact %s %i' % (haddocktools_path, ref, distance_threshold)
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
	for chain in contact_dic:
		for bound_res in contact_dic[chain]:
			try:
				unbound_res = numbering_dic[chain][bound_res]
				izone_l.append('ZONE %s%i-%s%i:%s%i-%s%i' % (chain, bound_res, chain, bound_res, chain, unbound_res, chain,unbound_res))
				out.write('ZONE %s%i-%s%i:%s%i-%s%i\n' % (chain, bound_res, chain, bound_res, chain, unbound_res, chain,unbound_res))
				# print 'ZONE %s%i-%s%i:%s%i-%s%i' % (chain, bound_res, chain, bound_res, chain, unbound_res, chain,unbound_res)
			except:
				print 'Res %i not found in unbound' % bound_res
			# print res
	out.close()
	izone_dic[ref] = izone_l

for stage in stage_ref_dic:
	####
	pdb_l = stage_ref_dic[stage][0] 
	ref = stage_ref_dic[stage][1]
	atoms = stage_ref_dic[stage][2]
	izone_l = izone_dic[ref]

	print '>> stage %s' % stage

	# prepare structural input
	irms_dic = {}
	for conformation in pdb_l:
		#####
		# fix chain

		fix_chain_segid(conformation)

		# prepare cmd for PROFIT
		cmd = 'refe %s\nmobi %s\nATOMS %s\nZONE CLEAR\n%s\nstatus\nFIT\nquit' % (ref, conformation, atoms, '\n'.join(izone_l))
		# open('idbg','w').write(cmd)
		# exit()
		# run!
		output = os.popen('echo "%s" | profit' % cmd)
		# parse result
		result = [l for l in output if 'RMS' in l][0]
		#
		irms = float(result.split()[-1])
		#
		irms_dic[conformation] = irms
		result_dic[stage][conformation]['irms'] = irms

	#
	if stage == 'water':
		outputf = '%s/structures/it1/%s/i-RMSD.dat' % (runf, stage)
	else:
		outputf = '%s/structures/%s/i-RMSD.dat' % (runf, stage)
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
	os.system('cp %s %s' % (outputf, outputf.replace('.dat', '-sorted.dat')))


#=========================================================================================#
## Ligand RMSD
#=========================================================================================#

# print '> l-rmsd'

# ligand_zone = {}
# for chain in numbering_dic:
# 	ligand_zone[chain] = []
# 	for bound_res in numbering_dic[chain]:
# 		unbound_res = numbering_dic[chain][bound_res]
# 		#
# 		ligand_zone[chain].append('ZONE %s%s-%s%i:%s%i-%s%i' % (chain, bound_res, chain, bound_res, chain, unbound_res, chain, unbound_res))

# # generate command
# lrms_cmd = ''
# lrms_cmd += '\n'.join(ligand_zone[receptor_chain])
# lrms_cmd += '\n'
# lrms_cmd += 'FIT'
# lrms_cmd += '\n'
# for ligand in ligand_zone:
# 	if ligand != receptor_chain:
# 		l_tbw = ''
# 		for zone in ligand_zone[ligand]:
# 			l_tbw += ' R%s\n' % zone
# 		lrms_cmd += l_tbw[1:]
# 		lrms_cmd += '\n'
# lrms_cmd += 'ZONE CLEAR'
# lrms_cmd += '\n'

# # ready?
# for stage in stage_ref_dic:
# 	print '>>> stage %s' % stage

# 	pdb_l = stage_ref_dic[stage][0] 
# 	ref = stage_ref_dic[stage][1]
# 	atoms = stage_ref_dic[stage][2]

# 	lrms_dic = {}
# 	for conformation in pdb_l:

# 		# segid_output = 'segid.temp'
# 		fix_chain_segid(conformation)

# 		# os.system('%s/pdb_segid-to-chain %s > %s' % (haddocktools_path, conformation, segid_output))
# 		# os.system('cp segid.temp %s' % conformation)
# 		cmd = 'refe %s\nmobi %s\nATOMS %s\n%s\nquit' % (ref, conformation, atoms, lrms_cmd)

# 		output = os.popen('echo "%s" | profit' % cmd)

# 		# parse result
# 		result = [l for l in output if 'RMS' in l][-1]
# 		lrms = float(result.split()[-1])

# 		lrms_dic[conformation] = lrms
# 		result_dic[stage][conformation]['lrms'] = lrms
# 		#
# 		# os.system('rm %s' % segid_output)

# 	if stage == 'water':
# 		outputf = 'run2/structures/it1/%s/l-RMSD.dat' % stage
# 	else:
# 		outputf = 'run2/structures/%s/l-RMSD.dat' % stage
# 	#
# 	lrms_out = open(outputf,'w')
# 	lrms_out.write('#struc l-RMSD\n')
# 	sorted_lrms_dic = sorted(lrms_dic.items(), key=operator.itemgetter(1))
# 	for e in sorted_lrms_dic:
# 		conformation = e[0]
# 		pdb_name = conformation.split('/')[-1]
# 		lrms = e[1]
# 		lrms_out.write('%s %.3f\n' % (conformation, lrms))
# 	lrms_out.close()
# 	#
# 	os.system('cp %s %s' % (outputf, outputf.replace('.dat', '-sorted.dat')))

#=========================================================================================#
## Fnat
#=========================================================================================#

print '> fnat'

# define contact for AA and for CG

def get_contact_list(contactf):
	contact_list = []
	for l in open(contactf):
		resnumA,chainA,atomA,resnumB,chainB,atomB,distance = l.split()
		contact_list.append( ((int(resnumA),chainA,atomA), (int(resnumB),chainB,atomB)) )
		contact_list.append( ((int(resnumB),chainB,atomB), (int(resnumA),chainA,atomA)) )
	return contact_list

distance_threshold = 5.0

contact_dic = {}
for ref in [pdbf, pdbf_cg]:
	#
	contact_outf = ref.replace('.pdb', '.contacts')
	cmd = '%s/contact %s %i' % (haddocktools_path, ref, distance_threshold)
	run(cmd, contact_outf)
	#
	bound_contact_list = get_contact_list(contact_outf)
	# 
	# fix numbering and ignore contacts seen only in reference
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
			print contact, 'discarded, not found on unbound'
	#
	contact_dic[ref] = fixed_contact_list


for stage in stage_ref_dic:

	pdb_l = stage_ref_dic[stage][0] 
	ref = stage_ref_dic[stage][1]

	print '>>> stage %s' % stage

	fnat_dic = {}
	for conformation in pdb_l:
		###
		fix_chain_segid(conformation)

		# distance_threshold = 5.0
		contact_outf = conformation.replace('.pdb', '.contacts')
		cmd = '%s/contact %s %i' % (haddocktools_path, conformation, distance_threshold)
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

#==========#

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
		# full_name = 'run2/structures/%s/%s'% (stage, pdb_name)
		full_name = haddock_s_f.replace('file.list', pdb_name)
		haddock_score_dic[stage][full_name] = score

	# get energies and etc
	pdb_l = stage_ref_dic[stage][0]
	for conformation in pdb_l:
		# print pdb
		data = open(conformation).readlines()
		energies_l = map(float, data[7].split(':')[-1].split(','))
		total, bonds, angles, improper, dihe, vdw, elec, air, cdih, coup, rdcs, vean, dani, xpcs, rg = energies_l
		buried = float(data[32].split(':')[-1])
		desolv = float(data[27].split(':')[-1])
		binding = float(data[30].split(':')[-1])
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
		result_dic[stage][conformation]['buried'] = buried
		result_dic[stage][conformation]['desolv'] = desolv
		result_dic[stage][conformation]['binding'] = binding


for stage in result_dic:
	out = open('%s/%s.dat' % (runf, stage),'w')
	out.write('stage\tpdb_name\trank\tscore\tfnat\tlrms\tirms\tbinding\tdesolv\tbinding\ttotal\tbonds\tangles\timproper\tdihe\tvdw\telec\tair\tcdih\tcoup\trdcs\tvean\tdani\txpcs\trg\n')
	# out = open('%s.capri' % stage, 'w')
	# out.write('conformation\tfnat\tlrms\tirms\n')
	# pdb_name = 
	sorted_haddock_score_list = sorted(haddock_score_dic[stage].items(), key=operator.itemgetter(1))
	for i, e in enumerate(sorted_haddock_score_list):
		#
		conformation = e[0]
		rank = i+1
		#
		fnat = result_dic[stage][conformation]['fnat']
		lrms = result_dic[stage][conformation]['lrms']
		irms = result_dic[stage][conformation]['irms']
		#
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
		buried = result_dic[stage][conformation]['buried'] 
		desolv = result_dic[stage][conformation]['desolv'] 
		binding = result_dic[stage][conformation]['binding']
		#
		haddock_score = haddock_score_dic[stage][conformation]
		#
		out.write('%s\t%s\t%i\t%.4f\t%.3f\t%.2f\t%.2f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\n' % (stage, conformation, rank, haddock_score, fnat, lrms, irms,
			binding,
			desolv,
			binding, 
			total, bonds, angles, improper, dihe, vdw, elec, air, cdih, coup, rdcs, vean, dani, xpcs, rg))
	#
	out.close()


#=========================================================================================#
# Clustering
#=========================================================================================#

# water

os.chdir('%s/structures/it1/water/analysis' % runf)
if not os.path.isfile('cluster.out'):
	os.system('gunzip cluster.out.gz')
os.chdir('../')
os.system('~/ana_clusters.csh -best 4 analysis/cluster.out')
# it1
os.chdir('../analysis')
if not os.path.isfile('cluster.out'):
	os.system('gunzip cluster.out.gz')
os.chdir('../')
os.system('~/ana_clusters.csh -best 4 analysis/cluster.out')
os.chdir('../../../')
os.system('~/results-stats.csh %s' % runf)
# cmd = '/home/rodrigo/results-stats.csh %s' % runf
# run(cmd, '%s.stats' % runf)







