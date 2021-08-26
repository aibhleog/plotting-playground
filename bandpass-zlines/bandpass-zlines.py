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

# if you want to run this script in your terminal via an alias, edit this variable
# with the path to this directory -- then you can run the script as a command from
# any location on your computer and it will work perfectly!
path = '/path/to/file/' # include the '/' at the end!

def bandpass_zlines(redshift):
	import numpy as np
	import matplotlib.pyplot as plt
	import igm_absorption as igm # 	another script written by Taylor Hutchison
				     #	which adds in IGM absorption for the higher redshifts
	import os

	def lines(ax,yo,z,text='yes'):
		# plotting relevant lines -- feel free to add more!
		lines = {'lya':[1215.67,r'Ly$\alpha$'],'nv':[1240,'NV $\lambda$1240'],
			'civ':[1548,'CIV $\lambda$1549'],'heii1':[1640.4,'HeII $\lambda$1640'],
			'oiii]':[1664,'OIII] $\lambda$1660,1666'],
			'siiii]':[1883,'SiIII] $\lambda$1883,1892'],
			'ciii]':[1906.8,'CIII] $\lambda$1907\n  & $\lambda$1909'],
			'mgii':[2798,'MgII $\lambda$2796\n  & $\lambda$2803'],
			'[oii]':[3727,'[OII] $\lambda$3727\n    & $\lambda$3729'],
			'[neiii]':[3869,'[NeIII] $\lambda$3869'],'heii2':[4686,'HeII $\lambda$4686'],
			'hbeta':[4862.68,r'H$\beta$ $\lambda$4863'],'[oiii]1':[4959,''],
			'[oiii]2':[5007,'[OIII] $\lambda$4959\n    & $\lambda$5007'],
			'hei':[5876,'HeI $\lambda$5876'],'hdelta':[4102,'H$\delta$'],
			'hgamma':[4341,'H$\gamma$']}
		
		shifts = {'lya':[-140,yo+yo*2.8],'nv':[40,yo],
			'civ':[-90,yo-yo*0.4],'heii1':[-70,yo+yo*1.4],
			'oiii]':[25,yo-yo*0.2],'siiii]':[-85,yo-yo*0.5],
			'ciii]':[50,yo+yo*0.4],'mgii':[40,yo],
			'[oii]':[-180,yo],'[neiii]':[-80,yo],'heii2':[-100,yo],
			'hbeta':[-105,yo+yo*0.8],'[oiii]1':[40,yo],
			'[oiii]2':[70,yo],'hei':[-100,yo],'hdelta':[40,yo],'hgamma':[40,yo]}
		
		line_names = list(lines.keys()) # just to get the list of all of the lines
		for l in line_names: # walking through the lines
			shift, y = shifts[l] # accessing shifts for line
			wave,name = lines[l] # accessing line info for line
		
			ax.axvline(wave/1e4*(1+z),ls='--',color='k',alpha=.5)
			if text == 'yes':
				if l == 'heii1' or l == 'oiii]': font = 13
				else: font = 15
				ax.text((wave+shift)/1e4*(1+z),y,'%s'%(name),\
					fontsize=font,verticalalignment='bottom',rotation='vertical')


	# Cloudy model provided by Taylor Hutchison
	# Single stellar population from BPASS with age=10Myr & IMF that goes to 100 Msolar, 
	# Z(stellar)=Z(nebular)=0.2 Zsolar, ionization parameter log_10(U)=-2.1, n_H=300 cm^(-3)	
	z,zneb,u = 0.2,0.2,-2.1
	model = 'age7z%szneb%su%s_100.con'%(z,zneb,u)
	data = '' # if you place it somewhere else, you can put the path here
	con = np.loadtxt(data+model,usecols=[0,6])
	wave,vfv = con[:,0],con[:,1]
	#print(wave[0]*1e4,wave[-1]*1e4)
	nu = 2.998e+14 / wave
	sed_0 = vfv / nu

	# plotting the redshifted spectrum
	plt.figure(figsize=(16.5,5))
	ax = plt.gca()

	# ------ reading in filter curves ------ #
	# HST/WFC3 NIR photometric bandpasses	
	f105w = np.loadtxt(path+'HST-WFC3_IR.F105W.dat')
	f160w = np.loadtxt(path+'HST-WFC3_IR.F160W.dat')

	# Keck/MOSFIRE NIR spectroscopic bandpasses
	mos_y = np.loadtxt(path+'mosfire_yband_throughput.txt')
	mos_j = np.loadtxt(path+'mosfire_jband_throughput.txt')
	mos_h = np.loadtxt(path+'mosfire_hband_throughput.txt')
	mos_k = np.loadtxt(path+'mosfire_kband_throughput.txt')
	mos_j[:,0] *= 1e4 # because everything else
	mos_k[:,0] *= 1e4 # is in Angstroms

	# Spitzer/IRAC IR channels
	spitzer36 = np.loadtxt(path+'Spitzer_IRAC.I1.dat')
	spitzer45 = np.loadtxt(path+'Spitzer_IRAC.I2.dat')
	spitzer58 = np.loadtxt(path+'Spitzer_IRAC.I3.dat')
	spitzer80 = np.loadtxt(path+'Spitzer_IRAC.I4.dat')
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

	ax.set_yscale('log')
	ax.set_yticklabels([])
	ax.tick_params(labelsize=16)
	ax.set_xlabel(f'observed wavelength for $z=\,${redshift} [microns]',fontsize=16)
	ax.set_xlim(0.08*(1+redshift),0.668*(1+redshift))
	ax.set_ylim(1e-15,3.5e-13)
	
	leg = ax.legend(frameon=False,loc=9,fontsize=13,ncol=len(filts),\
		bbox_to_anchor=(0.5,1.12))
	for lh in leg.legendHandles: 
		lh.set_alpha(1)

	plt.tight_layout()
	plt.savefig(path+'figure.pdf')
	plt.close('all')

	# opening image from the terminal
	os.system(f'gnome-open {path}figure.pdf')


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





