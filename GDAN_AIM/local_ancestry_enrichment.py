#!/usr/bin/python -u
from __future__ import division
import sys, getopt
import re
import numpy as np
import argparse, os, sys
from scipy import stats
import math
import matplotlib
import matplotlib.pyplot as plt
matplotlib.pyplot.switch_backend('agg')
from scipy.stats import mannwhitneyu
import pandas as pd
import patsy

input1 = str(sys.argv[1])
input2=open("gdan_aim_patient_ancestry_calls.txt")

positions={}
for line in (raw.strip().split() for raw in input1):
	key = line[0]
	positions[key] = "\t".join(line)

eur_pop={}
afr_pop={}
### find admixed information. ###
for line in (raw.strip().split() for raw in input2):
	if "patient" not in line[0]:
		if "NA" not in line[len(line)-4]:
			if (float(line[len(line)-4]) > 0.2) and (float(line[len(line)-4]) < 0.8):
				if (float(line[len(line)-5]) > 0.2) and (float(line[len(line)-5]) < 0.8):
					if line[1] in cantype:
						(sampleID, tumor_type, consensus_call) = line[0:3]
						if ("asian" not in line[2]) and ("sas" not in line[2]):
							eur_pop["TCGA-"+str(sampleID)]=line[len(line)-5]
							afr_pop["TCGA-"+str(sampleID)]=line[len(line)-4]


### look for local ancestry for each region stored in positions. ####
lol={}
files=[]
for line in (raw.strip().split() for raw in samplelist):
		files.append(line[0])

for sample in afr_pop:
			print "working on", sample 
			inputfile4 = sample+"_A.bed"
			if inputfile4 in files:
				input4=open(inputfile4)	
				for line2 in (raw.strip().split() for raw in input4):
					for key in positions:
						chrom=key.split(":")[0]
						pos1=key.split(":")[1]
						if (str(line2[0]) == chrom) and (int(line2[1]) < int(pos1)) and (int(line2[2]) > int(pos1)):
							if "EUR" in line2[3]:
								a1=0
							if "AFR" in line2[3]:
								a1=1
							inputfile5 = sample+"_B.bed"
							if inputfile5 in files:
								input5=open(inputfile5)
								for line3 in (raw.strip().split() for raw in input5):
									if (str(line3[0]) == chrom) and (int(line3[1]) < int(pos1)) and (int(line3[2]) > int(pos1)):
										if "EUR" in line3[3]:
											if key in lol:
												if a1 == 0:
													lol[key]=int(lol[key])+0
												if a1 == 1:
													lol[key]=int(lol[key])+1
											else:
												if a1 == 0:
													lol[key]=0
												if a1 == 1:
													lol[key]=1
										if "AFR" in line3[3]:
											if key in lol:
												if a1 == 0:
													lol[key]=int(lol[key])+1
												if a1 == 1:
													lol[key]=int(lol[key])+2	
											else:
												if a1 == 0:
													lol[key]=1
												if a1 == 1:
													lol[key]=2

### perform the enrichment test. ###													
pos={}; score={}
for key in lol:
	chr1, pos1 = key.split(":")
	if chr1 in pos:
		pos[chr1]=pos[chr1]+";"+str(pos1)
		score[chr1]=score[chr1]+";"+str(lol[key])
	else:
		pos[chr1]=str(pos1)
		score[chr1]=str(lol[key])

to_plot_chr=[]; to_plot_pos=[]; to_plot_score_n=[]
for i in pos:
	pos_n=pos[i].split(";")
	score_n=score[i].split(";")
	chr_n=np.array([i]*len(pos_n))
	to_plot_chr=np.concatenate((to_plot_chr, chr_n), axis=0)
	to_plot_pos=np.concatenate((to_plot_pos, pos_n), axis=0)
	to_plot_score_n=np.concatenate((to_plot_score_n, score_n), axis=0)

zscore = stats.zscore(np.array(to_plot_score_n).astype(float))

df = pd.DataFrame({"A": to_plot_chr, "B": to_plot_pos, "Z": zscore})
df.to_csv('TCGA_geno/analysis/admix_local_'+str("_".join(cantype))+'_block_all.zscores.v2.txt', sep='\t')
