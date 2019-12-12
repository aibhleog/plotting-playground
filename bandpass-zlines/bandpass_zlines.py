'''
This is a script that can be implemented into your .bashrc and used
to plot a redshifted spectrum and show relevant lines of interest.
--> NOTE that this outputs a PDF file, but feel free to change to PNG

As Taylor mostly works in the NIR and IR, the bandpasses plotted only
cover that wavelength space, although this code can easily be adapted
to fit your needs.

One possible way to do this would be, based upon the redshift and 
resulting spectral range covered, you could only plot the bandpasses
that would show up there.  That could cut down on the number of
unnecessary filters shown in your legend.

Filters for most every telescope/instrument pair can be found using
the SVO Filter Profile Service:
http://svo2.cab.inta-csic.es/svo/theory/fps3/

Planned updates:  I would like to add a quiescent spectrum eventually.
                  
Credit: 	Taylor Hutchison
		aibhleog@tamu.edu
		Texas A&M University
'''

_author_ = 'Taylor Hutchison'

def bandpass_zlines(redshift):
	import numpy as np
	import matplotlib.pyplot as plt
	import igm_absorption as igm # 	another script written by Taylor Hutchison
				     #	which adds in IGM absorption for the higher redshifts
	import os

	def lines(ax,yo,z,text='yes'):
		# plotting relevant lines -- feel free to add more!
		lines = [1215.67,1240,1640.4,1883,1906.8,2798,3727,4862.68,\
					4959,5007.0,1548.48,4686,5876,3869,4102,4341]
		lnames = [r'Ly$\alpha$','NV $\lambda$1240','HeII $\lambda$1640',\
				'SiIII] $\lambda$1883\n  & $\lambda$1892',\
				'CIII] $\lambda$1907\n  & $\lambda$1909',\
				'MgII $\lambda$2796\n  & $\lambda$2803',\
				'[OII] $\lambda$3727\n    & $\lambda$3729',\
				r'H$\beta$ $\lambda$4863','','[OIII] $\lambda$4959\n    & $\lambda$5007',\
				'CIV $\lambda$1549','HeII $\lambda$4686','HeI $\lambda$5876',\
				'[NeIII] $\lambda$3869','H$\delta$','H$\gamma$']
		font = 15
		for i in range(len(lines)):
			if i == 1: shift = 50; y = yo
			elif i == 2: shift = 30	; y = yo-yo*0.7
			elif i == 3: shift = -180; y = yo+yo*1.4
			elif i == 6: shift = -180
			elif i == 7: shift = -105; y = yo+yo*0.8
			elif i == 9: shift = 80; y = yo
			elif i == 4: shift = 60; y = yo+yo*0.4
			elif i == 0: shift = -140; y = yo+yo*2.8
			elif i == len(lines)-6: shift = -100; y = yo
			elif i == len(lines)-5: shift = -100; y = yo
			elif i == len(lines)-4: shift = -110; y = yo
			elif i == len(lines)-3: shift = -80
			else: shift = 40; y = yo
			ax.axvline(lines[i]/1e4*(1+z),ls='--',color='k',alpha=.5)
			if text == 'yes':
				ax.text((lines[i]+shift)/1e4*(1+z),y,'%s'%(lnames[i]),\
					fontsize=font,verticalalignment='bottom',rotation='vertical')

	# Cloudy model provided by Taylor Hutchison
	# Single stellar population from BPASS with age=10Myr & IMF that goes to 100 Msolar, 
	# Z(stellar)=Z(nebular)=0.2 Zsolar, ionization parameter log_10(U)=-2.1, n_H=300 cm^(-3)	
	z,zneb,u = 0.2,0.2,-2.1
	model = 'age7z%szneb%su%s_100.con'%(z,zneb,u)
	data = '/home/aibhleog/Desktop/catalogs/cloudy/models/steidel/single_cont_100/'
	con = np.loadtxt(data+model,usecols=[0,6])
	wave,vfv = con[:,0],con[:,1]
	#print(wave[0]*1e4,wave[-1]*1e4)
	nu = 2.998e+14 / wave
	sed_0 = vfv / nu

	# plotting the redshifted spectrum
	plt.figure(figsize=(14.5,5))
	ax = plt.gca()
	ax = plt.axes(xlim=(0.08*(1+redshift),0.599*(1+redshift)),ylim=(1e-15,3.5e-13))

	# ------ reading in filter curves ------ #
	# HST/WFC3 NIR photometric bandpasses	
	f105w = np.loadtxt('HST-WFC3_IR.F105W.dat')
	f160w = np.loadtxt('HST-WFC3_IR.F160W.dat')

	# Keck/MOSFIRE NIR spectroscopic bandpasses
	mos_y = np.loadtxt('mosfire_yband_throughput.txt')
	mos_j = np.loadtxt('mosfire_jband_throughput.txt')
	mos_h = np.loadtxt('mosfire_hband_throughput.txt')
	mos_k = np.loadtxt('mosfire_kband_throughput.txt')
	mos_j[:,0] *= 1e4 # because everything else
	mos_k[:,0] *= 1e4 # is in Angstroms

	# Spitzer/IRAC IR channels
	spitzer36 = np.loadtxt('Spitzer_IRAC.I1.dat')
	spitzer45 = np.loadtxt('Spitzer_IRAC.I2.dat')
	spitzer58 = np.loadtxt('Spitzer_IRAC.I3.dat')
	spitzer80 = np.loadtxt('Spitzer_IRAC.I4.dat')
	# ALL FILTER CURVES (except Keck/MOSFIRE) can be found at 
	# http://svo2.cab.inta-csic.es/svo/theory/fps3/

	count = 0
	# this just provides the colors for the filters and their names for the legend
	filts = ['MOS Y','MOS J','MOS H','MOS K',\
			'F105W','F160W','[3.6]','[4.5]','[5.8]','[8.0]']
	fcolors = ['#1F618D','C0','#5DADE2','C9','none','none',\
				'#F4D03F','#DA9B27','#DA7B27','#DA4027']
	flines = ['#1F618D','C0','#5DADE2','C9','#1FAF2F','#7ED487',\
				'#F4D03F','#DA9B27','#DA7B27','#DA4027']
	for filt in [mos_y,mos_j,mos_h,mos_k,f105w,f160w,spitzer36,\
						spitzer45,spitzer58,spitzer80]:
		indx = np.arange(len(filt[:,0]))
		indx = indx[filt[:,0] > 0]
		scale = (1e-14/max(filt[:,1][indx]))
		plt.fill_between(filt[:,0][indx]/1e4,filt[:,1][indx]*scale,0,alpha=0.3,zorder=0,\
			label=filts[count],facecolor=fcolors[count],edgecolor=flines[count])
		plt.plot(filt[:,0][indx]/1e4,filt[:,1][indx]*scale,alpha=0.8,color=flines[count])
		count += 1
	# -------------------------------------- #

	# applying IGM absorption depending upon z
	sed = sed_0 * igm.igm_absorption(wave*1e4*(1+redshift),redshift)
	ax.plot(wave*(1+redshift),sed,color='k',lw=2.)
	lines(ax,2e-14,redshift) # adding in the line labels

	plt.yscale('log')
	ax.set_yticklabels([])
	ax.tick_params(labelsize=16)
	ax.set_xlabel('observed wavelength for $z=\,$%s [microns]'%redshift,fontsize=16)
	leg = ax.legend(frameon=False,loc=9,fontsize=13,ncol=len(filts),\
		bbox_to_anchor=(0.5,1.12))
	for lh in leg.legendHandles: 
		lh.set_alpha(1)

	plt.tight_layout()
	plt.savefig('figure.pdf')
	plt.close('all')

	# opening image from the terminal
	os.system('gnome-open figure.pdf')


# reads in input for scripted version
if __name__ == "__main__":
	import sys
	try:
		if sys.argv[1] == 'help':
			print('''
Given a redshift, this command will show a spectrum that
has been redshifted with relevant lines marked. In addition,
it will show relevant NIR and IR bandpasses.

Use the following notation:   zlines [redshift]
''')	
		else: bandpass_zlines(float(sys.argv[1]))
	except IndexError: # if you don't list a redshift
		z = 7.5032 # my favorite redshift, see Hutchison et al. 2019
		print('Redshift not specified, set to z=7.5032',end='\n\n')
		bandpass_zlines(z)





