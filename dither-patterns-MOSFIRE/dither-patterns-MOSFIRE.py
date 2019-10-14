'''
This script makes an animation that of the ABAB dither pattern for the
MOSFIRE spectrograph on Keck I.  This includes the helpful information
about where it is recommended to place your object in the slit.

SOMETIMES it's easier to animate using a function and the `animation`
package in `matplotlib`, however in cases like this, when you need to
fine-tune detail for each frame (and there aren't too many frames) it's
actually better to just make images and then combine them into a GIF.

----->	Note that this code makes ten images.  In the README associated 
	with this directory you'll find instructions for how to make the
	the images into an animation.

Credit: 	Taylor Hutchison
		aibhleog@tamu.edu
		Texas A&M University
'''

_author_ = 'Taylor Hutchison'

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import matplotlib.patheffects as PathEffects # it's how you make black-outlined text!

# running through making the ten images
for i in range(10):
	# making figure
	plt.figure(figsize=(9,6))
	ax = plt.gca()
	ax = plt.axes(xlim=(-0.6,1.75),ylim=(-0.4,1.2))

	# common kwargs for annotations
	notes_kwargs = {'transform':ax.transAxes,'fontsize':17}
	titles_kwargs = {'transform':ax.transAxes,'fontsize':19}

	# slit
	slit = Rectangle((-0.2,-0.3), 0.35, 1.35, facecolor='none',edgecolor='k',lw=2.7)
	ax.add_artist(slit)

	# -- stationary -- #
	if i == 0 or i == 1:
		# adding a star
		star = Circle((-0.02,0.6),0.03,facecolor='#F4D03F',edgecolor='k',lw=2.2,zorder=10)
		ax.add_artist(star)
		
		# -- adding notations -- #
		if i == 1: 
			txt = ax.text(0.4,0.7,'object in slit',color='#F4D03F',**titles_kwargs)
			txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])
			ax.plot([0.045,0.31],[0.62,0.735],color='k',lw=2) # line to object
		
	# -- first dither -- #
	if i == 2 or i == 4:
		fill = Rectangle((-0.2,0),0.35,1.05,zorder=0,facecolor='#ADCBAD',edgecolor='k',lw=2.5,ls='--')
		ax.add_artist(fill)

		# adding a star
		star = Circle((-0.02,0.6),0.03,facecolor='#F4D03F',edgecolor='k',lw=2.2,zorder=10)
		ax.add_artist(star)

		# -- adding notations -- #
		ax.plot([0.18,0.32],[0.65,0.74],color='k',lw=2)	
		txt = ax.text(0.4,0.7,'Dither A',color='#71976F',**titles_kwargs)
		txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])

	# -- second dither -- #
	if i == 3 or i == 5:
		fill = Rectangle((-0.2,-0.3),0.35,1.05,zorder=0,facecolor='#ADCBAD',edgecolor='k',lw=2.5,ls='--')
		ax.add_artist(fill)

		# adding a star
		star = Circle((-0.02,0.3),0.03,facecolor='#F4D03F',edgecolor='k',lw=2.2,zorder=10)
		ax.add_artist(star)

		# -- adding notations -- #
		ax.plot([0.18,0.32],[0.33,0.42],color='k',lw=2)
		txt = ax.text(0.4,0.5,'Dither B',color='#71976F',**titles_kwargs)
		txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])

	# -- both dithers, showing safe space -- #
	if i >= 6 and i <= 8:
		# adding both stars
		star1 = Circle((-0.02,0.3),0.03,facecolor='#9C8218',edgecolor='k',lw=2.2,zorder=7)
		star2 = Circle((-0.02,0.6),0.03,facecolor='#9C8218',edgecolor='k',lw=2.2,zorder=7)
		ax.add_artist(star1); ax.add_artist(star2)
	
		fill = Rectangle((-0.2,0),0.35,0.75,zorder=0,facecolor='#C1DCEE',edgecolor='k',lw=2.5,ls='--')
		ax.add_artist(fill)
		
		# -- specifying 2.5" dither space -- #
		ax.errorbar(-0.26,0.9,yerr=0.13,uplims=True,lolims=True,lw=2,color='k')
		ax.text(0.12,0.768,'2.5" dither\nspace    ',ha='right',**notes_kwargs)
		ax.errorbar(-0.26,0.-0.15,yerr=0.13,uplims=True,lolims=True,lw=2,color='k')
		ax.text(0.12,0.12,'2.5" dither\nspace    ',ha='right',**notes_kwargs)
		
		# notes about safe region
		if i == 6:
			# -- adding notations -- #
			ax.plot([0.034,0.305],[0.32,0.64],color='k',lw=2) # line to star 1
			ax.plot([0.04,0.305],[0.61,0.64],color='k',lw=2) # line to star 2
			txt = ax.text(0.4,0.6,'safe space in both dithers\n      for object location',transform=ax.transAxes,fontsize=20,color='#5DADE2')
			txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])
	
		# adding center star
		elif i == 7:
			star3 = Circle((-0.02,0.45),0.03,facecolor='#F4DC7F',edgecolor='k',lw=2.2,zorder=7)
			ax.add_artist(star3)
			
			# -- adding notations -- #
			ax.plot([0.04,0.305],[0.465,0.64],color='k',lw=2) # line to star 3
			txt = ax.text(0.4,0.6,'location of object\n   in final stack',transform=ax.transAxes,fontsize=20,color='#5DADE2')
			txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])
			
		# marking the dither amplitudes from center
		elif i == 8:
			star3 = Circle((-0.02,0.45),0.03,facecolor='#F4DC7F',edgecolor='k',lw=2.2,zorder=7)
			ax.add_artist(star3)
			
			# -- specifying 1.5" dithers -- #
			ax.errorbar(0.07,0.525,yerr=0.057,uplims=True,lolims=True,lw=2,color='k')
			ax.text(0.335,0.565,'+1.5" dither',**notes_kwargs)
			ax.errorbar(0.07,0.367,yerr=0.057,uplims=True,lolims=True,lw=2,color='k')
			ax.text(0.335,0.465,'$-$1.5" dither',**notes_kwargs)
		
	# -- do not place star here -- #	
	if i == 9:
		# adding bad star
		star4 = Circle((-0.02,0.75),0.03,facecolor='#9C3918',edgecolor='k',lw=2.2,zorder=7)
		ax.add_artist(star4)
		
		fill = Rectangle((-0.2,0),0.35,0.75,zorder=0,facecolor='#C1DCEE',edgecolor='k',lw=2.5,ls='--')
		ax.add_artist(fill)
		
		txt = ax.text(0.4,0.6,'DO NOT PUT\nOBJECT HERE',transform=ax.transAxes,fontsize=20,color='#9C3918')
		txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])
		

	# turning off grid lines
	ax.axis('off')

	plt.tight_layout() # good practice, makes figures nicer
	plt.savefig(f'frame_{i}.png') # fyi, my matplotlibrc has dpi=300
	plt.close('all')














