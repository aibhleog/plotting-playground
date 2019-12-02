'''
This script makes a figure showing Spitzer/IRAC colors for redshifted model
spectra. For this figure, the Spitzer/IRAC [3.6]-[4.5] colors are shown for
binary stellar population models and single stellar population models for a
large range of ionization parameters.
---> The stellar population models are BPASS models (Eldridge et al. 2017).

The models used are some of my Cloudy simulations (v17, Ferland et al. 2017).
The files read into this script are the calculated Spitzer/IRAC colors from
those models.

Credit: 	Taylor Hutchison
			aibhleog@tamu.edu
			Texas A&M University
'''

_author_ = 'Taylor Hutchison'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# reading in Spitzer/IRAC bandpasses
irac36 = np.loadtxt('Spitzer_IRAC.I1.dat')
irac45 = np.loadtxt('Spitzer_IRAC.I2.dat')
#irac45 = oldirac45[oldirac45[:,1]>0.0015] # just to fix the odd bandpass shape


# Spitzer/IRAC colors calcuated for redshift Cloudy+BPASS models
# --------------------------------------------------------------
# Cloudy model provided by Taylor Hutchison
# binary stellar population from BPASS with age=10Myr & IMF that goes
# to 300 Msolar, Z(stellar)=Z(nebular)=0.1 Zsolar, n_H=300 cm^(-3)
# (note: log_10(U)=-1.5 is a very high ionization parameter, and
#        and log_10(U)=-3.5 is a more typical ionization parameter)
files_binary_models = ['irac_color_BPASS_bin_u-3.5_Z-0.1.txt',\
					   'irac_color_BPASS_bin_u-2.5_Z-0.1.txt',\
					   'irac_color_BPASS_bin_u-1.5_Z-0.1.txt']
files_single_models = ['irac_color_BPASS_no-bin_u-3.5_Z-0.1.txt',\
					   'irac_color_BPASS_no-bin_u-2.5_Z-0.1.txt',\
					   'irac_color_BPASS_no-bin_u-1.5_Z-0.1.txt']

# reading in the files (just the second column, the IRAC colors)
binary_models = [np.loadtxt(files_binary_models[0])[1],
				 np.loadtxt(files_binary_models[1])[1],
				 np.loadtxt(files_binary_models[2])[1]]
single_models = [np.loadtxt(files_single_models[0])[1],
				 np.loadtxt(files_single_models[1])[1],
				 np.loadtxt(files_single_models[2])[1]]


# making the figure
plt.figure(figsize=(11,7))
gs1 = gridspec.GridSpec(2,1,height_ratios=[2,1.25],hspace=0.03) # I love gridspec

zed = np.linspace(1,10,num=100) # range of redshift from 1 to 10
cmap = [plt.get_cmap('Blues'),plt.get_cmap('Reds')] # colormaps for Binary & Single
fold = ['binary_cont_300','single_cont_100'] # BPASS stellar population models
name = ['with binaries, M$_{up}$: 300 M$_{\odot}$','no binaries, M$_{up}$: 100 M$_{\odot}$']

# top subplot
ax = plt.subplot(gs1[0])

models = [binary_models,single_models] # less code to loop it
for i in range(2):
	colors = [cmap[i](j) for j in np.linspace(0,1,7)]
	colors = colors[1:]
	
	kwargs = {'edgecolor':'k','s':100}
	ax.scatter(zed,models[i][0],color=colors[0],label='U: -1.5',**kwargs)
	ax.scatter(zed,models[i][1],color=colors[2],label='U: -2.5',**kwargs)
	ax.scatter(zed,models[i][2],color=colors[4],label='U: -3.5',**kwargs)


# we're going to make two different legends & a note about the metallicity
ax.text(0.02,0.9,'$Z_* = Z_{neb} = 0.1$ $Z_\odot$',transform=ax.transAxes,fontsize=16)
ax.axhline(0,ls=':',color='k',zorder=0) # to guide the eye
ax.text(0.05,0.11,name[0],transform=ax.transAxes,fontsize=14) # "with binaries"    
ax.text(0.05,0.035,name[1],transform=ax.transAxes,fontsize=14) # "no binaries"
ax.scatter(1.25,-1.17,s=80,color='C0',edgecolor='k') # color for "with binaries"
ax.scatter(1.25,-1.37,s=80,color=colors[2],edgecolor='k') # color for "no binaries"
	
ax.legend(loc=4,ncol=2,fontsize=15,columnspacing=0.3,handletextpad=0.2,frameon=True)
# you can look up some fun legend() kwargs here:
# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html#matplotlib.pyplot.legend

ax.set_ylabel('[3.6]$\endash$[4.5]',fontsize=18)
ax.set_xticklabels([]) # because it's the top subplot and we don't need to see them
ax.set_xlim(zed[0],zed[-1]) # just to make sure the two subplots are consistent xranges
	
	
# bottom subplot
ax = plt.subplot(gs1[1])

# finding regions where transmission curves for CH1 & CH2
# would allow lines to be seen (so above 0.3 for both)
# ------------------------------------------------------- #
lines = {'oii1':3726.1,'oii2':3728.8,'oiii1':4959,'oiii2':5007,'hbeta':4862.68,'ha':6562.8}
tag = ['oii1','oii2','hbeta','oiii1','oiii2','ha']
names = [r'[OII] $\lambda$3727',r'[OII] $\lambda$3729',r'[OIII] $\lambda$4959',\
		 r'[OIII] $\lambda$5007', r'H$\beta$ $\lambda$4863',r'H$\alpha$ $\lambda$6563']

yes36 = irac36[:,0].copy()
yes36 = yes36[irac36[:,1] > 0.3]

yes45 = irac45[:,0].copy()
yes45 = yes45[irac45[:,1] > 0.3]

def redshift(line,obs):
	return obs/line-1
def zlam(line,z):
	return line*(z+1)

for l in range(len(names)):
	beg = redshift(lines[tag[l]],yes36[0])
	end = redshift(lines[tag[l]],yes36[-1])
	ax.plot([beg,end],[l,l],lw=4.5,color='C0')
	
	beg = redshift(lines[tag[l]],yes45[0])
	end = redshift(lines[tag[l]],yes45[-1])
	ax.plot([beg,end],[l,l],lw=4.5,color='#C14219')
# ------------------------------------------------------- #
   
ax.plot([12,12],[l,l],lw=2.5,color='C0',label='[3.6]') # lazy way to make the legend
ax.plot([12,12],[l,l],lw=2.5,color='#C14219',label='[4.5]') # lazy way to make the legend
ax.legend(loc=2,fontsize=15,frameon=True)

ax.set_xlabel('redshift',fontsize=17)
ax.set_ylim(-1,6)
ax.set_xlim(zed[0],zed[-1]) # just to make sure the two subplots are consistent xranges
ax.set_yticks(np.arange(0,6)) # spacing it for the emission line names
ax.set_yticklabels(names)

plt.savefig('figure.pdf')
#plt.show()
plt.close('all')
