'''
This script makes an image very similar to those in Hutchison et al. 2024. 
I created this as a view of a range of values for integral field spectroscopic
data when looking at a spatially-resolved map and wanting to see the distribution.

Credit: 	Taylor Hutchison
			astro.hutchison@gmail.com
'''

_author_ = 'Taylor Hutchison'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from astropy.convolution import Gaussian2DKernel


# start by making fake data
data = Gaussian2DKernel(12).array * 3.5
clump = Gaussian2DKernel(5).array

# adding clumps, various stuff
std = 5
size = 8*5 + 1 # the resulting size of Gaussian2DKernel
data[int(size/2):int(size*1.5),size:size*2] += clump * 1.25
data[:size,:size] += clump * 1.5
data[size:size*2,int(size/2):int(size*1.5)] += clump * 0.25
data[data.shape[0]-size:,int(size/2):int(size*1.5)] += clump * 0.75
data[data.shape[0]-size:,int(size*1.3):int(size*1.3)+size] += clump


# adding some "no galaxy" regions for aesthetics
data[data<0.001] = np.nan
# rescaling data for vis purposes
data = np.log10(data)




# MAKING FIGURE
# ---------------
plt.figure(figsize=(10,6))
gs0 = gridspec.GridSpec(1,2,width_ratios=[2,1],wspace=-0.12) # if you use tight_layout it may yell


# the spatial map itself
ax = plt.subplot(gs0[0])
ax.axis('off')
ax.set_title("log$_{10}$U",y=0.94)

im = ax.imshow(data,origin='lower',cmap='viridis')
cax = plt.colorbar(im,pad=0.03)
cax.ax.yaxis.set_ticks_position("left")

# getting clims to help syncing colorbar & histogram
clims = [cax.vmin,cax.vmax]


# the histogram that links to the colorbar
ax = plt.subplot(gs0[1])
ax.axis('off')
ax.set_zorder(-1) # makes sure subplot dimensions don't cover previous one

n,bins,patches = ax.hist(data.flatten(),bins=40,orientation="horizontal")
ax.set_ylim(clims) # matching colorbar

# using this to color the histogram using the bins
# https://stackoverflow.com/questions/23061657/plot-histogram-with-colors-taken-from-colormap
bin_centers = 0.5 * (bins[:-1] + bins[1:])
cm = mpl.colormaps.get_cmap('viridis')

# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)

# setting colors
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))


# have to maually add y axis
ax.axhline(-2.15,color='k',lw=1)
for i in np.arange(20,121,20): # fiddle with this until you like the range, etc.
    ax.text(i+2,-2.115,i,ha='right',rotation=270,fontsize=13)
    ax.plot([i,i],[-2.135,-2.165],color='k',lw=1)


# adding median, if helpful
median = np.nanmedian(data)
ax.axhline(median,color='k',lw=2,ls='--')
ax.text(7,median+0.03,'median')


plt.tight_layout()
plt.savefig('figure.pdf')
plt.show()
plt.close('all')











































