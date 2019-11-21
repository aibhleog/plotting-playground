'''
This script makes a figure showing where redshifted emission lines pop up
in wavelength space. Under-plotted are the wavelength ranges of Keck/MOSFIRE 
and Spitzer/IRAC bandpasses.

Of course you can add more lines, especially ones you're more interested in!
Note though that there are some minor adjustments done for certain lines,
so if you do add in or replace particular line, be aware of that.

Credit: 	Taylor Hutchison
		aibhleog@tamu.edu
		Texas A&M University
'''

_author_ = 'Taylor Hutchison'

import numpy as np
import matplotlib.pyplot as plt

# Dictionary of lines
# currently holds the lines I use most frequently in my work
dic = {'ha':6562.8,'c.iii]':[1906.8,1908.73],'lya':1215.67,\
    'c.iv':[1548.19,1550.76],'o.ii':[3726.1,3728.8],'o.iii':[4959.,5007.],\
    'si.iii]':[1882.71,1892.03],'cii':2326.0,'mg.ii':[2795.53,2802.71],\
    'n.v':[1238.82,1242.8],'o.iii]':[1660.81,1666.15],'he.i':5876,\
    'ne.v':3426,'si.iv':1397.61,'he.ii':1640.4,'he.i':[3889,5876],\
    's.ii':[6717,6731],'hbeta':4862.68,'ne.iii':3869.81,'n.ii':[6549.81,6585.23],\
    'si.iv+o.iv]':1400,'niv]':1486,'hdelta':4102.89,'hgamma':4341.68}


# Describing MOSFIRE, HST, and IRAC bandpasses
# use band[:,1] > 0.3 as a throughput cut

# ------ reading in filter curves ------ #
# -------------------------------------- #
# Keck/MOSFIRE NIR spectroscopic bandpasses
mos_y = np.loadtxt('mosfire_yband_throughput.txt')
mos_j = np.loadtxt('mosfire_jband_throughput.txt')
mos_h = np.loadtxt('mosfire_hband_throughput.txt')
mos_k = np.loadtxt('mosfire_kband_throughput.txt')

# Spitzer/IRAC IR channels
spitzer36 = np.loadtxt('Spitzer_IRAC.I1.dat')
spitzer45 = np.loadtxt('Spitzer_IRAC.I2.dat')
spitzer58 = np.loadtxt('Spitzer_IRAC.I3.dat')
spitzer80 = np.loadtxt('Spitzer_IRAC.I4.dat')
# ALL FILTER CURVES (except Keck/MOSFIRE) can be found at 
# http://svo2.cab.inta-csic.es/svo/theory/fps3/
# -------------------------------------- #


# Redshifting emission lines & plotting bandpass coverage
# making the dictionary keys for the lines I care about
lines = ['lya','n.v','c.iv','he.ii','o.iii]','si.iii]','c.iii]','o.ii','hbeta','o.iii','n.ii','ha']
names = [r'Ly$\alpha$','N$\,$V','C$\,$IV','He$\,$II','O$\,$III]','Si$\,$III]','C$\,$III]','[O$\,$II]',r'H$\beta$','[O$\,$III]','[N$\,$II]',r'H$\alpha$']
lst = ['-','--','-.',':','-','--','-.',':','-','--','-.',':']

cmap = plt.get_cmap('RdBu')
colors = [cmap(j) for j in np.linspace(0,1,len(lines))]
altcol = ['#ECC367','#5E6061','#70A5BC'] #'#84B6CC'
zed = np.linspace(1,10,num=100)
plt.figure(figsize=(10,5.5))
for i in range(len(lines)):
    #print('For %s: %s Angstroms'%(names[i],dic[lines[i]]))
    try:
        len(dic[lines[i]])
        if lines[i] == 'si.iii]' or lines[i] == 'c.iii]'\
            or lines[i] == 'o.ii':
            plt.plot((1+zed)*dic[lines[i]][0]/1e4,zed,color=altcol[i-5],\
                 label=names[i],ls=lst[i],lw=2.9)
        else:
            plt.plot((1+zed)*dic[lines[i]][0]/1e4,zed,color=colors[i],\
                 label=names[i],ls=lst[i],lw=2.9)
    except TypeError:
        plt.plot((1+zed)*dic[lines[i]]/1e4,zed,color=colors[i],\
                 label=names[i],ls=lst[i],lw=2.9)
        
# plotting regions for filters
filts = [mos_y,mos_j,mos_h,mos_k,spitzer36,spitzer45,spitzer58,spitzer80]
names = ['$Y$','$J$','$H$','$K_s$','[3.6]','[4.5]','[5.8]','[8.0]']
cmap = plt.get_cmap('Blues')
colors = [cmap(j) for j in np.linspace(0.1,1,len(filts))]

count = 0
for f in filts:
    wave,vals = f[:,0],f[:,1]
    scale = np.median(vals)-np.std(vals)*1.5
    wave,vals = wave[vals>scale],vals[vals>scale]
    if count == 1 or count == 3:  
        if count == 1:
            indx = np.arange(len(wave))
            indx = indx[vals>0.05]
            wave,vals = wave[indx],vals[indx]
        plt.axvspan(wave[0],wave[-1],alpha=0.4,color=colors[count],zorder=0)
        plt.axvline(wave[0],alpha=0.5,color='k',zorder=0)
        plt.axvline(wave[-1],alpha=0.5,color='k',zorder=0)
        plt.text(np.mean(wave)-np.mean(wave)*count/37,10.2,names[count],fontsize=15)
    else:
        plt.axvspan(wave[0]/1e4,wave[-1]/1e4,alpha=0.4,color=colors[count],zorder=0)
        plt.axvline(wave[0]/1e4,alpha=0.5,color='k',zorder=0)
        plt.axvline(wave[-1]/1e4,alpha=0.5,color='k',zorder=0)
        if count != len(filts)-1: 
            plt.text((min(wave)+min(wave)*(count/200))/1e4,10.2,names[count],fontsize=15)
        else:
            plt.text((min(wave)+min(wave)*(count/80))/1e4,10.2,names[count],fontsize=15)
    count += 1

plt.legend()
plt.xscale('log')
plt.ylabel('redshift',fontsize=17)
plt.xlabel('observed wavelength [microns]',fontsize=16)
plt.gca().set_xticklabels(['','','1.','10.'])
plt.ylim(1,10)

plt.tight_layout()
plt.savefig('figure.pdf')
#plt.show()
plt.close('all')



