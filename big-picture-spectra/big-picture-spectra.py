'''
This script makes an image very similar to Figure 2 of Hutchison et al. 2019 (https://arxiv.org/pdf/1905.08812.pdf). Undoubtedly, there are likely simpler ways to make this figure -- this is how I chose to code it up.

Because the figure in the paper uses some proprietary data, the code below will generate fake data to be plotted.

Credit: 	Taylor Hutchison
		aibhleog@tamu.edu
		Texas A&M University
'''

_author_ = 'Taylor Hutchison'

import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
import matplotlib.gridspec as gridspec
from matplotlib.patches import Polygon
import matplotlib.patheffects as PathEffects
from mpl_toolkits.axes_grid.inset_locator import inset_axes
from matplotlib.lines import Line2D
from matplotlib import patches

# -- Generating fake data -- #
# -------------------------- #
np.random.seed(seed=3) # fixing the random seed so we can get the same result

gauss2d = np.loadtxt('gaussian2D_sig2_kernel7.txt') # fake 1D emission line
gauss1d = np.loadtxt('gaussian1D_sig2_kernel7.txt') # fake 2D emission line
# 1D & 2D gaussian pulled from here (because it's faster for this exercise):
# http://dev.theomader.com/gaussian-kernel-calculator/

noise1d = np.random.uniform(-1,1,250) # noise for 1D spectrum
noise2d = np.random.uniform(-1,1,(250,70)) # noise for 2D spectrum
shape = noise2d.shape
xcen, ycen = int(shape[0]/2), int(shape[1]/2)

galspec2d_line1 = noise2d.copy()
galspec2d_line1[xcen-3:xcen+4,ycen-3:ycen+4] += gauss2d * 35 # 2D emission line
galspec1d_line1 = noise1d.copy()
galspec1d_line1[xcen-3:xcen+4] += gauss1d * 15 # Lya 1D emission line

galspec2d_line2 = galspec2d_line1.copy()
galspec2d_line2[xcen+17:xcen+24,ycen-3:ycen+4] += gauss2d * 35 # 2D emission line
galspec1d_line2 = galspec1d_line1.copy()
galspec1d_line2[xcen+17:xcen+24] += gauss1d * 10 # CIII] 1D doublet emission line

noisegal = np.random.uniform(-1,1,(50,35)) # noise for photometry of 'galaxy'
galaxy = noisegal.copy()
galaxy[22:29,13:20] += gauss2d * 25 # add signal for galaxy shape
galaxy[24:31,16:23] += gauss2d * 25 # add signal for galaxy shape

wavelength = np.arange(len(galspec1d_line1)) # fake wavelength range

# fake errors
np.random.seed(seed=13) # fixing the random seed so we can get the same result
error1d = np.random.random(len(noise1d)) + 0.4
# ---------------------------#



# -- Initializing the image -- #
# ---------------------------- #
f = plt.figure(figsize=(10.5,9))
gs0 = gridspec.GridSpec(2,1,height_ratios=[1,0.9],hspace=0.1) # the main subplots


# ------------- #
# -- TOP ROW -- #
# ------------- #

gs01 = gridspec.GridSpecFromSubplotSpec(1,2,subplot_spec=gs0[0], # the top panel's subplots
								width_ratios=[1.2,2],wspace=0.22)

# --> RIGHT SIDE: the Lya spectrum
line = 'lya'
band = 'Y'

# The subplot gs001 is made up of 3 subplots where the top and bottom are just used to
# center the middle one more accurately -- they aren't necessary if you don't care THAT much :)
gs001 = gridspec.GridSpecFromSubplotSpec(3,1,subplot_spec=gs01[1],
							height_ratios=[0.05,1,0.12],hspace=0.0)
# This is the real subplot for the data (the middle one from gs001), split into 2 subplots
# so that we can have the 2D spectrum on top and the 1D on the bottom
gs011 = gridspec.GridSpecFromSubplotSpec(2,1,subplot_spec=gs001[1], 
							height_ratios=[1.25,2],hspace=0.0)

# 2D spectrum
ax01 = plt.Subplot(f, gs011[0])
ax01.imshow(galspec2d_line1[75:175,28:42].T, # zooming in for the sake of the example
            aspect='auto',origin='lower',cmap='gray',clim=(-1.5,2.3))

# removing the tickmarks and labels for the 2D spectrum
ax01.xaxis.set_ticks_position('none')
ax01.yaxis.set_ticks_position('none')
ax01.set_yticklabels([])
ax01.set_xticklabels([])

# white text with black outline
txt = ax01.text(0.023,0.73,'%s-band'%(band), size=20.5, color='w',transform=ax01.transAxes)
txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='k')])
f.add_subplot(ax01) # adds the subplot to the image

# 1D spectrum
ax02 = plt.Subplot(f, gs011[1])
ax02.step(wavelength,galspec1d_line1,where='mid',lw=2.3)
ax02.fill_between(wavelength,error1d,error1d*-1,alpha=0.2)

ax02.set_xlim(wavelength[74],wavelength[174])
ax02.set_ylabel(r'F$_{\lambda}$ [10$^{-18}$ erg/s/cm$^2$/$\AA$]',fontsize=16)
ax02.set_xlabel('observed wavelength [microns]',labelpad=5,fontsize=16)
f.add_subplot(ax02) # adds the subplot to the image


# --> LEFT SIDE: F160W STAMP
gs011 = gridspec.GridSpecFromSubplotSpec(1,1,subplot_spec=gs01[0])
ax011 = plt.Subplot(f, gs011[0]) # no need to add extra tiny subplots for padding here!
ax011.imshow(galaxy,aspect='auto',origin='upper',cmap='gray',clim=(-1,2))

# removing the tickmarks and labels for the 2D spectrum
ax011.xaxis.set_ticks_position('none')
ax011.yaxis.set_ticks_position('none')
ax011.set_yticklabels([])
ax011.set_xticklabels([])

# white text with black outline
txt = ax011.text(0.03,0.90,'F160W',ha='left',size=22.5, color='w',transform=ax011.transAxes)
txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='k')])

# adding years for the slit layouts, using the set_path_effects to "bold" the text
txt = ax011.text(0.04,0.13,'2016',size=16+3.5, color='#CF6060',transform=ax011.transAxes)
txt.set_path_effects([PathEffects.withStroke(linewidth=1.18, foreground='#CF6060')])
txt = ax011.text(0.04,0.22,'2014',size=16+3.5, color='#F4D03F',transform=ax011.transAxes)
txt.set_path_effects([PathEffects.withStroke(linewidth=1.18, foreground='#F4D03F')])
txt = ax011.text(0.04,0.04,'2017',size=16+3.5, color='#70B5E3',transform=ax011.transAxes)
txt.set_path_effects([PathEffects.withStroke(linewidth=1.18, foreground='#70B5E3')])


# plotting slits over the regions in the image
                        # loc: 2,    3,          4,        1
ax011.add_patch(Polygon([[7,7],[22,45],[25.5,43],[11,5]], # 2016 slit
						zorder=3,facecolor='none',lw=1.8,edgecolor='#CF6060'))
ax011.add_patch(Polygon([[15,5],[15,45],[20,45],[20,5]], # 2014 slit
						zorder=3,facecolor='none',lw=1.8,edgecolor='#F4D03F'))
ax011.add_patch(Polygon([[5,23],[5,28],[28,28],[28,23]], # 2017 slit
						zorder=3,facecolor='none',lw=1.8,edgecolor='#70B5E3'))

f.add_subplot(ax011) # adds the subplot to the figure
# ------------------------------------------------------------------------- #


# ---------------- #
# -- BOTTOM ROW -- #
# ---------------- #

# --> the CIII] spectrum
line = 'ciii'
band = 'H'

# similar padding process done as with the Lya spectrum (where only the middle one matters)
gs2 = gridspec.GridSpecFromSubplotSpec(1,3,subplot_spec=gs0[1],width_ratios=[0.28,2,0.13],wspace=0.0)

# splitting the middle subplot from above into two, so that we can have 2D on top and 1D on bottom
gs11 = gridspec.GridSpecFromSubplotSpec(2,1,subplot_spec=gs2[1],height_ratios=[1.75,2],hspace=0.0)

# 2D spectrum
ax11 = plt.Subplot(f, gs11[0])
ax11.imshow(galspec2d_line2[:,15:55].T,aspect='auto',origin='lower',cmap='gray',clim=(-1.5,2.2))

# removing the tickmarks and labels for the 2D spectrum
ax11.xaxis.set_ticks_position('none')
ax11.yaxis.set_ticks_position('none')
ax11.set_yticklabels([])
ax11.set_xticklabels([])

# white text with black outline
txt = ax11.text(0.02,0.75,'%s-band'%(band), size=16+8.5, color='w',transform=ax11.transAxes)
txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='k')])
f.add_subplot(ax11) # adds subplot to the figure


# 1D spectrum
ax12 = plt.Subplot(f, gs11[1])
ax12.step(wavelength,galspec1d_line2,where='mid',lw=2.7)
ax12.fill_between(wavelength,error1d,error1d*-1,alpha=0.2)

ax12.set_xlim(wavelength[0],wavelength[-1])
ax12.set_ylabel(r'F$_{\lambda}$ [10$^{-19}$ erg/s/cm$^{2}$/$\AA$]',fontsize=16)
ax12.set_xlabel('observed wavelength [microns]',fontsize=16)
f.add_subplot(ax12) # adds subplot to the figure

# saving figure
plt.savefig('figure.pdf')
#plt.show()
plt.close('all')





