'''
This is a script which adds in IGM absorption 
for the higher redshifts, following the prescription
outlined in Madau (1995, ApJ, 441, 18).

Note that the four different absorption effects
accounted for here only include the first four
transitions in the Lyman series (alpha to delta).

Credit: 	Taylor Hutchison
		aibhleog@tamu.edu
		Texas A&M University
'''

import numpy as np

def lya_forest(lam,z): # in angstroms
	lam_a = 1216   
	output = []
	for i in range(len(lam)):
		if lam[i] < lam_a*(1+z):
			val = 0.0036 * np.power(lam[i]/lam_a,3.46)
			output.append(val)
		else:
			output.append(0)
	return output

def metal_lines(lam,z): # in angstroms
	lam_a = 1216  
	output = []
	for i in range(len(lam)):
		if lam[i] < lam_a*(1+z):
			val = 0.0017 * np.power(lam[i]/lam_a,1.68)
			output.append(val)
		else:
			output.append(0)
	return output

def line_blanketing(lam,z): # in angstroms
	Aj = [1.7e-3,1.2e-3,9.3e-4]
	lam_j = [1026,973,950] # angstroms
	output = []
	for i in range(len(lam)):
		val = 0
		if lam[i] < (lam_j[0]*(1+z)):
			val += Aj[0]*np.power(lam[i]/lam_j[0],3.46)
		if lam[i] < (lam_j[1]*(1+z)):
			val += Aj[1]*np.power(lam[i]/lam_j[1],3.46)
		if lam[i] < (lam_j[2]*(1+z)):
			val += Aj[2]*np.power(lam[i]/lam_j[2],3.46)
	output.append(val)
	return output

def lyman_limit(lam,z):
	ly_L = 912 # angstroms
	output = []
	for i in range(len(lam)):
		x_c = 1 + ((lam[i]/ly_L)-1)
		x_em = 1 + z
		val = 0
		if lam[i] < ly_L*(1+z):
			val += 0.25 * x_c**3 * (x_em**0.46 - x_c**0.46) \
				+ 9.4 * x_c**1.5 * (x_em**0.18 - x_c**0.18) \
				- 0.7 * x_c**3 * (x_c**-1.32 - x_em**-1.32) - 0.023 \
				* (x_em**1.68 - x_c**1.68)
	output.append(val)
	return output

def igm_absorption(lam,z):
	tau_eff = np.asarray(lya_forest(lam,z)) \
		+ np.asarray(metal_lines(lam,z)) \
		+ np.asarray(line_blanketing(lam,z)) \
		+ np.asarray(lyman_limit(lam,z))
	tau_eff[lam > 1216*(1+z)] = min(tau_eff)*1e-2
	return np.exp(-tau_eff) # to be multiplied by a source's spectrum
		
		
		
		
		
