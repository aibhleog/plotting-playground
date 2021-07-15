'''
This script makes an animation that redshifts a spectrum and, upon reaching
6.5 < z < ~11 marks the Epoch of Reionization. The spectrum that gets shifted
is a model of mine from a Cloudy simulation (v17, Ferland et al. 2017).
--->  It takes a minute or two so be patient! (it's the animation package) 

Additionally, I have included a module that applies IGM attentuation to the
spectrum as it shifts to larger redshifts.

Using the animation package requires a learning curve, so be sure to google
any time you encounter a problem or want to add something and you don't
know the proper notation!

Planned updates:  Improving the colored backgrounds for UV and NIR.
                  I would like to add a quiescent spectrum eventually.
                  --> *may* make that spectrum disappear after it reaches
                      a certain redshift (for example, past z>6?)

Credit: 	Taylor Hutchison
		aibhleog@tamu.edu
		Texas A&M University
'''

_author_ = 'Taylor Hutchison'

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt # timing how long it takes
from matplotlib.patches import Circle
from matplotlib import collections
import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import igm_absorption as igm # 	another script written by Taylor Hutchison
			     #	which adds in IGM absorption for the higher redshifts

# adding a timer to this to see how long it takes
start_it = dt.now()
print('\nStarting timer', start_it)


fig = plt.figure(figsize=(10,6))
ax = plt.gca()
ax = plt.axes(xlim=(0.1,2),ylim=(4e-16,1e-13))

# Cloudy model provided by Taylor Hutchison
# binary stellar population from BPASS with age=10Myr & IMF that goes to 300 Msolar, 
# Z(stellar)=Z(nebular)=0.1 Zsolar, ionization parameter log_10(U)=-1.5, n_H=300 cm^(-3)
# (note: this is a very low Z and high ionization model)
con = np.loadtxt('age7z0.1zneb0.1u-1.5_300.con',usecols=[0,6])
wave,vfv = con[:,0],con[:,1]
nu = 2.998e+14 / wave
sed_0 = vfv / nu

# this is my way of applying a rainbow for the visual band
cmap = cm.get_cmap('rainbow')
vcolors = [cmap(i) for i in np.linspace(0,1,300)]
x = np.linspace(0.39,0.71,num=300)
for i in range(len(x)):
	if i < len(x)-1:
		ax.axvspan(x[i],x[i+1],color=vcolors[i])#,alpha=0.75)

# marking the UV and NIR wavelength ranges 
x = np.linspace(0.71,2.5,num=300)
ax.axvspan(0.71,x[148],color=vcolors[-4]) # NIR
for i in range(len(x[:50])):
	scale = i/len(x)
	ax.axvspan(x[i],x[50],color='#900C3F',alpha=scale) # NIR
ax.axvspan(x[50],2.5,color='#900C3F')	

x = np.linspace(0.1,0.401,num=70)
ax.axvspan(x[32],0.4,color=vcolors[3]) # UV
for i in range(len(x[50:])):
	scale = (len(x[50:])-i)/(len(x)*1.5)
	ax.axvspan(x[50],x[50+i],color='#5A1B82',alpha=scale) # UV
ax.axvspan(0.1,x[50],color='#5A1B82')


# labeling all of the wavelength ranges
ax.text(0.05,0.08,'UV',fontsize=25,transform=ax.transAxes)
ax.text(0.17,0.08,'Visual',fontsize=25,transform=ax.transAxes)
ax.text(0.44,0.08,'Near-Infrared',fontsize=25,transform=ax.transAxes)

redshift = np.arange(0,10,0.2)
line, = ax.plot(wave,sed_0,lw=3.,color='k')
tex = ax.text(0.95,0.88,'',ha='right',transform=ax.transAxes,fontsize=28)

# need an initial setup function so the animation function can
# anchor off of it -- this is essential!
def init():
	global tex
	line.set_data(wave,sed_0)
	tex.set_text('$z$: 0')
	return line,tex,

# the function that will actually be changing things in the animation
def shift(r):
	# applies IGM absorption depending upon the redshift
	sed = sed_0 * igm.igm_absorption(wave*1e4*(1+redshift[r]),redshift[r])
	line.set_data(wave*(1+redshift[r]),sed/(1+(redshift[r]*0.3)))
	tex.set_text('$z$: %s'%(round(redshift[r],3)))
	
	# if you want the "Epoch of Reionization" to pop up at z>6.4, uncomment below
	#if redshift[r] > 6.4:
	#	ax.axvspan(0.9,1.5,alpha=0.07)
	#if redshift[r] > 6.4 and redshift[r] < 6.8:
	#	ax.text(0.47,0.75,'  Epoch of\nReionization',fontsize=25,transform=ax.transAxes)
	
	return line,tex,

# all the build up lead to this! Running the animation function...
anim = animation.FuncAnimation(fig,shift,init_func=init,\
	frames=np.arange(len(redshift)),interval=100,blit=True)

plt.yscale('log')
ax.set_yticklabels([])
ax.tick_params(labelsize=18)
ax.set_xlabel('wavelength [microns]',fontsize=19)

plt.tight_layout()
anim.save('figure.gif', fps=10, writer='imagemagick',dpi=150) # this will take a while to make
#plt.show() # WON'T WORK WITH JUPYTER LAB
plt.close('all')


print(f'That took: {dt.now()-start_it}')
