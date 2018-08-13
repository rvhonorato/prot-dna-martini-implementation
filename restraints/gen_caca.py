# generate CA-CA unambig restraints
import sys, argparse

parser = argparse.ArgumentParser()

parser.add_argument("contact_file", type=str,
                    help="File containing contact information")

args = parser.parse_args()

for l in open(args.contact_file).readlines():
   resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
   if atomA == 'CA' and atomB == 'CA':
   	print 'assign (name CA and segid %s and resi %s) (name CA and segid %s and resi %s) %.4f 0.500 0.500' % (chainA, resA, chainB, resB, float(dist))
