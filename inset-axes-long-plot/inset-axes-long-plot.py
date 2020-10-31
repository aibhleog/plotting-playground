'''
This script makes an image very similar to Figure 9 of Hutchison et al. 2019 
(https://arxiv.org/pdf/1905.08812.pdf). There may be simpler ways to make 
this figure, especially for the fine-tuning of the bandpass coverages on the
top of the figure -- this is how I chose to code it up.

The models used are some of my Cloudy simulations (v17, Ferland et al. 2017).
The original plot showed some JWST/NIRSpec simuated spectra for four of these
models, redshited to z = 7.5032 and scaled to H160 = 25.3 mag. However, for this
recreation of the plot, we'll just use one of the original models instead.

Credit: 	Taylor Hutchison
			aibhleog@tamu.edu
			Texas A&M University
'''

_author_ = 'Taylor Hutchison'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
from matplotlib.patches import Polygon
import matplotlib.patheffects as PathEffects
from mpl_toolkits.axes_grid.inset_locator import inset_axes

def lines(ax,y0):
	# plotting relevant lines
	z = 7.5027 # systemic redshift from Hutchison et al. (2019)
	lines = [1215.67,1240,1548.48,1640.4,1906.8,2798,3727,4686,4862.68,4959,5007]
	lnames = [r'Ly$\alpha$','NV $\lambda$1240','CIV $\lambda$1549','HeII $\lambda$1640',\
			'CIII] $\lambda$1907\n  & $\lambda$1909','MgII $\lambda$2798',\
			'[OII] $\lambda$3727\n    & $\lambda$3729', 'HeII $\lambda$4686',\
			r'H$\beta$ $\lambda$4863','','[OIII] $\lambda$4959\n    & $\lambda$5007']
			
	shiftme = [0,2,7,8]
	for i in range(len(lines)):
		# quick way to see if i is in the shiftme list
		# this will just allow you to move the text labels around
		if np.isin([i],shiftme)[0] == True: shift = -120
		else: shift = 50
		# now for the y values
		# you can add more `elif` lines if you want to shift other around
		if i == 0: y = y0*5.2 # to raise Lya up a lot
		else: y = y0
		
		ax.axvline(lines[i]/1e4*(1+z),ls='--',color='k',alpha=.5)
		ax.text((lines[i]+shift)/1e4*(1+z),y,'%s'%(lnames[i]),\
			fontsize=16,verticalalignment='bottom',rotation='vertical')
	
	
# names of JWST/NIRSpec dispersers/gratings
disp_filt = [['prism','clear'],['g140m','f070lp'],['g140m','f100lp'],\
		['g235m','f170lp'],['g395m','f290lp']]

# data parameters
colors = ['#962A13','k','#1F618D','#D1A90A']
# Cloudy model provided by Taylor Hutchison
# Single stellar population from BPASS with age=10Myr & IMF that goes to 100 Msolar, 
# Z(stellar)=Z(nebular)=0.2 Zsolar, ionization parameter log_10(U)=-2.1, n_H=300 cm^(-3)	
z,zneb,u = 0.2,0.2,-2.1
model = 'age7z%szneb%su%s_100.con'%(z,zneb,u)
data = '' # if you place it somewhere else, you can put the path here
con = np.loadtxt(data+model,usecols=[0,6]) # the Cloudy model, using only these columns
wave,vfv = con[:,0],con[:,1] # wavelength [microns], and SED [nu*F_nu]
nu = 2.998e+14 / wave # making frequency
spec = vfv / nu # now just F_nu
spec[spec == 0] = np.min(spec[spec>0]) # replacing any zeros with min (so log-space doesn't fail)
zwave = wave * 8.5032 # redshifted wavelength [microns]


# ----------------------- #
# -- making the figure -- #
# ----------------------- #
plt.figure(figsize=(13,5.5))
gs00 = gridspec.GridSpec(2,1,height_ratios=[0.23,1],hspace=0.0) # normally 0.4


# ------------------------------ #
# -- mapping out the gratings -- #
ax = plt.subplot(gs00[0])
ax.axis('off')

# prism
txt = ax.text(0.513,0.63+0.09,'PRISM',fontsize=15,transform=ax.transAxes)
txt.set_path_effects([PathEffects.withStroke(linewidth=0.4, foreground='k')])
ax.plot([0.6,2.76],[0.89,0.89],color='k',lw=2.)
ax.plot([3.13,5.3],[0.89,0.89],color='k',lw=2.)
ax.plot([0.601,0.601],[0.74,1.04],color='k',lw=1.7)
ax.plot([5.293,5.293],[0.74,1.04],color='k',lw=1.7)

# grism
y,alph = 0.1, ['A','B','C','D']
filts = [[0.7,1.27],[0.97,1.89],[1.66,3.17],[2.87,5.27]]
disp_filt = [['prism','clear'],['G140M','F070LP'],['G140M','F100LP'],\
		['G235M','F170LP'],['G395M','F290LP']]

# this section is a little messy but you get the idea
for i in [2,1,3]:
	x = np.median(filts[i])
	txt = ax.text(x-0.3,y-0.2,'%s/%s'%(disp_filt[i+1][0],disp_filt[i+1][1]),fontsize=14.5)
	txt.set_path_effects([PathEffects.withStroke(linewidth=0.4, foreground='k')])
		
	ax.plot([filts[i][0],x-0.32],[y,y],color='k',lw=2.)
	ax.plot([x+0.33,filts[i][1]],[y,y],color='k',lw=2.)
	ax.plot([filts[i][0],filts[i][0]],[y-0.15,y+0.15],color='k',lw=1.7)
	ax.plot([filts[i][1]+0.01,filts[i][1]+0.01],[y-0.15,y+0.15],color='k',lw=1.7)
	if i == 2: y -= 0.5
	
# the final grism bandpass plotted
i,y = 0,0.1
x = np.median(filts[i])
txt = ax.text(x-0.28,0.25,'%s/%s'%(disp_filt[i+1][0],disp_filt[i+1][1]),fontsize=13.5)
txt.set_path_effects([PathEffects.withStroke(linewidth=0.4, foreground='k')])
	
ax.plot([filts[i][0],filts[i][1]],[0.1,0.1],color='k',lw=2.)
ax.plot([filts[i][0],filts[i][0]],[-0.05,0.25],color='k',lw=1.7)
ax.plot([filts[i][1]+0.01,filts[i][1]+0.01],[-0.05,0.25],color='k',lw=1.7)

ax.set_ylim(-0.9,1.3)
ax.set_xlim(0.4,5.1)
ax.set_yticklabels([])
ax.set_xticklabels([])

# ------------------------------ #
# ------------------------------ #


# -- PRISM spectra -- #
ax1 = plt.subplot(gs00[1])

for j in range(4):
	sup_flux = spec.copy()
	sup_flux *= 1 + j*0.1 # just to stagger them
	sup_flux[zwave < 0.1215*8.5027] = 0 # no flux bluewards of Lya
	
	if j == 0: lab = '(%s)'%(j+1)
	else: lab = '(%s)'%(j+1)
	ax1.plot(zwave,sup_flux,color=colors[j],label=lab,lw=2.,zorder=3-j)

lines(ax1,9e-15) # adding lines
ax1.legend(fontsize=15.5,frameon=False,handlelength=1.,handletextpad=0.4,loc=1)
ax1.set_ylabel('flux [arbitrary units]',fontsize=17)	

plt.yscale('log')
ax1.set_yticklabels([])
ax1.tick_params(labelsize=16)
ax1.set_xlim(0.4,5.1)
ax1.set_ylim(8e-16,2e-13)
ax1.set_xlabel('observed wavelength [microns]',fontsize=17)
ax1.set_ylabel('flux [arbitrary units]',fontsize=17)

# ----------------- #


# --------------------------------- #
# ------ inset for NV zoom-in ----- #
# --------------------------------- #
inset = inset_axes(ax, width="8.1%", height=2.1,loc=3,\
	bbox_to_anchor=(0.019,0.08,1,1), bbox_transform=ax1.transAxes)
ax_01 = plt.gca()

for j in range(4):
	sup_flux = spec.copy()
	sup_flux *= 1 + j*0.1 # just to stagger them
	sup_flux[zwave < 0.1215*8.5027] = 0 # no flux bluewards
	
	ax_01.plot(zwave,sup_flux,color=colors[j],zorder=3-j)	

# adding the NV line by hand
ax_01.axvline(1240*8.5027/1e4,ls='--',color='k',alpha=.5)
ax_01.text(1235/1e4*8.5027,3.5e-15,'NV $\lambda$1240',fontsize=15.5,\
		verticalalignment='bottom',rotation='vertical')

ax_01.xaxis.set_ticks_position('none')
ax_01.yaxis.set_ticks_position('none')

ax_01.set_yscale('log')
ax_01.set_yticklabels([])
ax_01.set_xticklabels([])
ax_01.set_xlabel('medium res',fontsize=15)
ax_01.set_xlim(1.045,1.06)
ax_01.set_ylim(1e-15,2e-14)
# ------------ #

# ------------------------------------ #
# ------ inset for CIII] zoom-in ----- #
# ------------------------------------ #
inset = inset_axes(ax, width="8.4%", height=2.2,loc=8,\
	bbox_to_anchor=(-0.136,0.29,1,1), bbox_transform=ax1.transAxes)
ax_02 = plt.gca()

for j in range(4):
	sup_flux = spec.copy()
	sup_flux *= 1 + j*0.1 # just to stagger them
	sup_flux[zwave < 0.1215*8.5027] = 0 # no flux bluewards

	ax_02.plot(zwave,sup_flux,color=colors[j],lw=0.8,zorder=3-j)	

zlines = [1883,1894,1907,1909]
znames = ['SiIII] $\lambda$1883','SiIII] $\lambda$1892','[CIII]+CIII]','']
for l in range(len(zlines)): # adding the SiIII] and CIII] lines by hand
	ax_02.axvline(zlines[l]*8.5027/1e4,ls='--',color='k',alpha=.5)
	ax_02.text((zlines[l]-8)/1e4*8.5027,5e-15,znames[l],fontsize=14,\
		verticalalignment='bottom',rotation='vertical')

ax_02.xaxis.set_ticks_position('none')
ax_02.yaxis.set_ticks_position('none')

ax_02.set_yscale('log')
ax_02.set_yticklabels([])
ax_02.set_xticklabels([])
ax_02.set_xlabel('medium res',fontsize=15)
ax_02.xaxis.set_label_position('top') 
ax_02.set_xlim(1.59,1.63)
ax_02.set_ylim(1.5e-15,4e-14)
# ------------ #

plt.tight_layout()
plt.savefig('figure.pdf')
plt.close('all')



