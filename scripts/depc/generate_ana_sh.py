
import glob
benchmark_l = [e for e in glob.glob('*') if not 'txt' in e]

for root in benchmark_l:
	##############
	##############
	##############
	tbw = '''#PBS -q medium
#PBS -e /data/rodrigo/benchmark/%s/ana-cg.err
#PBS -o /data/rodrigo/benchmark/%s/ana-cg.out
#PBS -N %s-cg_ana

cd /data/rodrigo/benchmark/%s
python /home/rodrigo/Nostromo/scripts/ana-cg.py %s_complex.pdb run1
/home/rodrigo/Nostromo/scripts/results-stats.csh run1 > run1.stats''' % (root, root, root, root, root)
	out = open('%s/ana-cg.sh' % root,'w').write(tbw)
	##############
	##############
	##############
	tbw = '''#PBS -q medium
#PBS -e /data/rodrigo/benchmark/%s/ana-aa.err
#PBS -o /data/rodrigo/benchmark/%s/ana-aa.out
#PBS -N %s-aa_ana

cd /data/rodrigo/benchmark/%s
python /home/rodrigo/Nostromo/scripts/ana-cg.py %s_complex.pdb run2 --aa
/home/rodrigo/Nostromo/scripts/results-stats.csh run2 > run2.stats''' % (root, root, root, root, root)
	out = open('%s/ana-aa.sh' % root,'w').write(tbw)