#!/usr/bin/python

from __future__ import division

from __future__ import with_statement

import os, itertools, glob, sys

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
# from sklearn import metrics
from sklearn.metrics import roc_curve, auc
from numba import jit, typeof
from sys import stderr

def find_key(dic, val):
	return [k for k, v in dic.iteritems() if v == val][0]

def print_err(*args, **kwargs):
	sys.stderr.write(' '.join(map(str,args)) + '\n')
	

def frange(start, stop, step):

	'''Returns a list of floats given a start, stop and step'''

	weights = []
	x = start
	
	while x <= stop:
		weights.append(round(x,3))
		x += step

	#combinations = list(itertools.combinations_with_replacement(weights, 5))
	#return np.array(combinations)
	return weights


def parse_scores(scores_file):

	# read irmsd, elec, evdw, edesolv, eair, bsa and haddockscore from file

	with open(scores_file) as inp:
		# matrix = np.loadtxt(inp, usecols=(1, 2, 3, 4, 5, 6, 7)) # jroel
		matrix = np.loadtxt(inp, skiprows=1, usecols=(6, 16, 15, 8, 17, 9, 3)) 
		# irmsd, elec, vdw, desolv, air, bsa, hs
 	
	return matrix
	

# @jit(nopython=True)
def calculate_recall(irmsd, topN):

	'''Calculates the recall for a given top (topN) for a list of i-RMSD'''
	
	criteria = 4.0
	N_acceptable = 0
	T_acceptable = 0
	
	for r in list(irmsd):
		if r <= criteria:
			T_acceptable += 1
		else:
			continue
	
	for r in list(irmsd[0:topN]):
		if r <= criteria:
			N_acceptable += 1
		else:
			continue
	
	if N_acceptable == topN or N_acceptable == T_acceptable:
		recall = 1.0
	elif T_acceptable != topN:
		recall = N_acceptable / min(topN,T_acceptable)
	else:
		recall = 0.0
	
	return recall


# @jit(nopython=True)
def calculate_hits(irmsd, topN):

	'''Calculates the number of hits (good models according to a given criteria). It returns 1 if 
	#hits > minimum. 0 if #hits < minimum. Code for clustering purposes'''

	N_acceptable = 0
	criteria = 4.0
	minimum = 4
	# l = []
	for r in list(irmsd[:topN]):
		if r <= criteria:
			N_acceptable += 1
		
		# if N_acceptable >= minimum:
			# x = 1
		# else:
			# x = 0
		# l.append(x)
	
	return N_acceptable
			

# @jit(nopython=True)
def optimize_weights(energy_terms, matrix, combinations):

	'''MAIN FUNCTION. You may optimize for recall, AUC or min number of good models. NOTE: only 4 terms taken
		into consideration'''

	nr_models = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 225, 250, 275, 300, 325, 350, 375, 400]
	# nr_models = [200,400]
	
	# auc = np.zeros((len(combinations),))

	# recall_200 = np.zeros((len(combinations),))
	# recall_400 = np.zeros((len(combinations),))
	
	# cases_200 = np.zeros((len(combinations),))
	# cases_400 = np.zeros((len(combinations),))

	cases_200 = {}
	cases_400 = {}

	E_elec = energy_terms[:,0]
	E_vdw = energy_terms[:,1]
	E_desolv = energy_terms[:,2]
	BSA = energy_terms[:,3]

	irmsd = matrix[:,0]
	
	for n, combi in enumerate(combinations):
		
		# Calculate new haddock score using new weights
		w1,w2,w3,w4 = combi

		haddockscore = ( (E_elec * w1) + (E_vdw * w2) + (E_desolv * w3) + (BSA * w3) )
		
		# re-sort according to new score
		new = np.column_stack((irmsd, haddockscore))
		sorted = new[np.argsort(new[:, 1])]	
		sorted_irmsd = sorted[:, 0]
		#
		lim = 200
		e = []
		# print sorted_irmsd[0]
		for v in sorted_irmsd:
			if v <= 4.0:
				e.append((v, 1))
			else:
				e.append((v, 0))
		np.array(e)
		exit()

		#
		for n in nr_models:
			# TP # irms < 4.0 in top200
			tp = len([e for e in sorted_irmsd[:n] if e <= 4.0])
			# TN # irms > 4.0 not top200
			tn = len([e for e in sorted_irmsd[n:] if e >= 4.0])
			# FP # irms > 4.0 in top200
			fp = len([e for e in sorted_irmsd[:n] if e >= 4.0])
			# FN # irms < 4.0 not top200
			fn = len([e for e in sorted_irmsd[n:] if e <= 4.0])
			#
			tpr = float(tp) / float((tp + fn))
			fpr = float(fp) / float((fp + tn))
			#
			print 'tp: %i tn: %i fp: %i fn: %i' % (tp, tn, fp, fn)
			print 'tpr: %.2f fpr: %.2f' % (tpr, fpr)
		
		exit()
		cases_200[n] = calculate_hits(sorted_irmsd, 200)
		cases_400[n] = calculate_hits(sorted_irmsd, 400)
		# print calculate_hits(sorted_irmsd, 200)
		# exit()
	return cases_200, cases_400
	###################		

	
# if __name__ == '__main__':

Eelec_r = frange(0, 2, 0.1) #20
# Eelec_r = frange(0, 2, 0.5) 

Evdw_r = frange(0, 1, 0.05) #20
# Evdw_r = frange(0.5, 1.5, 0.05) 

Edesolv_r = frange(0, 2, 0.1) #20
#Edesolv = [2.0] * 20
BSA_r = frange(-1, 0, 0.05) #20
#BSA = [-0.2] * 20

Etotal = [Eelec_r, Evdw_r, Edesolv_r, BSA_r]

combinations = list(itertools.product(*Etotal))

file_list = glob.glob('*/run1/it0.dat')

bench_auc = []
bench_recalls200 = []
bench_recalls400 = []
bench_200 = []
bench_400 = []

for file in file_list:
	print file

	matrix = parse_scores(file)
	energy_terms = matrix[:, [2,3,4,6]]

	cases_200 = {}
	cases_400 = {}

	E_elec = energy_terms[:,0]
	E_vdw = energy_terms[:,1]
	E_desolv = energy_terms[:,2]
	BSA = energy_terms[:,3]

	irmsd = matrix[:,0]
	
	for n, combi in enumerate(combinations):
		
		# Calculate new haddock score using new weights
		w1,w2,w3,w4 = combi
		# vdw = 0.01
		# elec = 1.0 
		# desolv = 1.0
		# bsa = -0.01

		# haddockscore = ( (E_elec * w1) + (E_vdw * w2) + (E_desolv * w3) + (BSA * w3) )
		haddockscore = ( (E_elec * 1.0) + (E_vdw * 0.01) + (E_desolv * 1.0) + (BSA * -0.01) )
		
		# re-sort according to new score
		new = np.column_stack((irmsd, haddockscore))
		sorted = new[np.argsort(new[:, 1])]	
		sorted_irmsd = sorted[:, 0]
		#

		lim = 4.0
		approved = [e for e in sorted_irmsd[:200] if e <= lim]

		nrapproved = len(approved)
		nrdecoys = 200 - len(approved)
		if nrapproved == 0:
			# this combination did not select any model
			roc_auc = 0.0
		else:
			if nrdecoys == 0:
				nrdecoys = 200
			tpr = [0.0]  # true positive rate
			fpr = [0.0]  # false positive rate

			foundcandidate = 0.0
			founddecoys = 0.0
			for i, v in enumerate(sorted_irmsd[:200]):
				if v <= lim:
					foundcandidate += 1.0
				else:
					founddecoys += 1.0
				#
				tpr.append(foundcandidate / float(nrapproved))
				fpr.append(founddecoys / float(nrdecoys))


			roc_auc = auc(fpr, tpr) # compute area under the curve

		if roc_auc != 0.0:

			plt.figure(figsize=(4, 4), dpi=80)

			plt.xlabel("FPR", fontsize=14)
			plt.ylabel("TPR", fontsize=14)
			plt.title("ROC Curve", fontsize=14)
			plt.plot(fpr, tpr, color='black', linewidth=2, label='ROC curve (area = %0.2f)' % (roc_auc))
			# if randomline:
			x = [0.0, 1.0]
			plt.plot(x, x, linestyle='dashed', color='red', linewidth=2, label='random')

			plt.xlim(0.0, 1.0)
			plt.ylim(0.0, 1.0)
			plt.legend(fontsize=10, loc='best')
			plt.tight_layout()
			plt.savefig(file.split('/')[0]+'.png')
			plt.close()
			break
			# exit()


exit()
# AUC version #
# matrix_auc = np.array(bench_auc)
# matrix_recall200 = np.array(bench_recalls200)
# matrix_recall400 = np.array(bench_recalls400)
###################################
# Min n version #
# matrix_200 = np.array(bench_200)
# matrix_400 = np.array(bench_400)
###################################

d = {}
for n, combi in enumerate(combinations):

	# AUC version #
	# mean_auc = np.mean(matrix_auc[:,n])
	# mean_recall200 = np.mean(matrix_recall200[:,n])
	# mean_recall400 = np.mean(matrix_recall400[:,n])
	# print "STEP:", n, "AUC:", '%f' % mean_auc, "RECALL_200:", '%f' % mean_recall200, "RECALL_400:", '%f' % mean_recall400, "OPTIMIZATION_VECTOR:", combi
	###################################

	# Min n version #
	# N_200 = np.sum(matrix_200[:,n])
	# N_400 = np.sum(matrix_400[:,n])
	# print "STEP:", n, "N_200:", '%f' % N_200, "N_400:", '%f' % N_400, "OPTIMIZATION_VECTOR:", combi
	###################################
	v200 = np.median([e[n] for e in bench_200])
	# v200 = max([e[n] for e in bench_200])
	# mean_400 = np.median([e[n] for e in bench_400])
	# exit()
	# print "STEP:", n, mean_200, mean_400, combi 
	d[combi] = v200

m = max(d.values())
k = find_key(d, m)

print k, m