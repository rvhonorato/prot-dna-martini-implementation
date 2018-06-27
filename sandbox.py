import os, sys, glob, subprocess, time


def run(cmd, outputf):
	with open("./%s" % outputf, "w") as f:
		process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
		process.wait()

def run2(cmd, outputf):
	with open("./%s" % outputf, "w") as f:
		process = subprocess.Popen(cmd.split(), shell=False, stderr=f)
		process.wait()

cmd = 'tar zxf AAAAAG.tgz'
run(cmd,'log')
run2(cmd,'log')
open('log').readlines()